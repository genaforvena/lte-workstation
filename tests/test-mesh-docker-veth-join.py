#!/usr/bin/env python3
"""Regression: uniquely joined container peer ifindex resolves to its host veth."""
import importlib.machinery
import importlib.util
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "mesh-docker-veth-join"
LOADER = importlib.machinery.SourceFileLoader("mesh_docker_veth_join", str(SCRIPT))
SPEC = importlib.util.spec_from_loader("mesh_docker_veth_join", LOADER)
observer = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(observer)


class JoinFixtureTest(unittest.TestCase):
    def test_unique_peer_ifindex_maps_to_host_veth_devpath_and_task_label(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            proc = root / "proc" / "4242" / "root" / "sys" / "class" / "net"
            (proc / "eth0").mkdir(parents=True)
            (proc / "eth0" / "ifindex").write_text("37\n")
            host = root / "sys" / "class" / "net"
            host.mkdir(parents=True)
            target = root / "sys" / "devices" / "virtual" / "net" / "vethfixture"
            target.mkdir(parents=True)
            (target / "iflink").write_text("37\n")
            (host / "vethfixture").symlink_to(target)

            inspected = {
                "Id": "c" * 64,
                "State": {"Pid": 4242},
                "Config": {"Labels": {"mesh.task.key": "chain/step"}},
                "NetworkSettings": {"Networks": {"bridge": {"NetworkID": "net-1", "EndpointID": "endpoint-1"}}},
            }
            event = {
                "Type": "network",
                "Action": "connect",
                "Actor": {"ID": "net-1", "Attributes": {"container": "c" * 64, "name": "bridge"}},
                "time": 123,
                "timeNano": 123000000000,
            }

            row = observer.join_event(event, inspected, proc_root=root / "proc", host_net=host)

            self.assertEqual(row["container_id"], "c" * 64)
            self.assertEqual(row["endpoint_network"], "bridge")
            self.assertEqual(row["endpoint_id"], "endpoint-1")
            self.assertEqual(row["peer_ifindex"], 37)
            self.assertEqual(row["host_veth_devpath"], "/devices/virtual/net/vethfixture")
            self.assertEqual(row["mesh_task_key"], "chain/step")

    def test_ambiguous_endpoint_does_not_claim_a_peer_or_veth(self):
        inspected = {
            "Id": "d" * 64,
            "State": {"Pid": 4242},
            "Config": {"Labels": {}},
            "NetworkSettings": {"Networks": {"bridge": {}, "other": {}}},
        }
        event = {
            "Type": "network", "Action": "connect",
            "Actor": {"ID": "net-1", "Attributes": {"container": "d" * 64, "name": "bridge"}},
            "time": 123, "timeNano": 123000000000,
        }
        row = observer.join_event(event, inspected, proc_root=Path("/no/proc"), host_net=Path("/no/net"))
        self.assertEqual(row["peer_ifindex"], "UNKNOWN")
        self.assertEqual(row["host_veth_devpath"], "UNKNOWN")
        self.assertEqual(row["mesh_task_key"], "UNKNOWN")

    def test_duplicate_host_iflink_does_not_pick_the_first_veth(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            proc = root / "proc" / "4242" / "root" / "sys" / "class" / "net"
            (proc / "eth0").mkdir(parents=True)
            (proc / "eth0" / "ifindex").write_text("37\n")
            host = root / "sys" / "class" / "net"
            host.mkdir(parents=True)
            for name in ("veth-one", "veth-two"):
                target = root / "sys" / "devices" / "virtual" / "net" / name
                target.mkdir(parents=True)
                (target / "iflink").write_text("37\n")
                (host / name).symlink_to(target)
            inspected = {
                "State": {"Pid": 4242},
                "Config": {"Labels": {}},
                "NetworkSettings": {"Networks": {"bridge": {"NetworkID": "net-1"}}},
            }
            event = {
                "Type": "network", "Action": "connect",
                "Actor": {"ID": "net-1", "Attributes": {"container": "e" * 64, "name": "bridge"}},
                "time": 123,
            }
            row = observer.join_event(event, inspected, proc_root=root / "proc", host_net=host)
            self.assertEqual(row["join_status"], "ambiguous")
            self.assertEqual(row["peer_ifindex"], "UNKNOWN")
            self.assertEqual(row["host_veth_devpath"], "UNKNOWN")


if __name__ == "__main__":
    unittest.main()
