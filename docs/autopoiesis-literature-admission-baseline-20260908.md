# Literature-task admission baseline

Date: 2026-09-08T10:23Z  
Source: `/home/mesh-home/.mesh/ideas-queue`  
Consumer: proposed autopoietic `mesh-task` creator in
`autopoiesis-task-ledger-20260908`.

## Acceptance predicate

An unresolved `STUDY` row is directly admissible only when it explicitly has
all six fields proposed by the design: origin kind, stable source, hypothesis,
concrete question, acceptance predicate, and feedback disposition. Fields are
counted only when stated in the material; they are not inferred from suggestive
prose.

## Result

Eight unresolved `STUDY` rows were sampled. **0/8 passed (0%).** All eight name
an origin kind and dated study brief, but none states a falsifiable hypothesis,
a concrete question, an acceptance predicate, or a feedback disposition.

| queue line | row SHA-256 | kind | source | hypothesis | question | acceptance | feedback | pass |
|---:|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 6 | `7f539d134974e2e3b37213b8fbe355c9f2c7b680878ed54be930de77bb8e3903` | yes | yes | no | no | no | no | no |
| 7 | `fc83d6befa1834e84aea244ecb77a649f3e718f118cd64fcbcfca46c4cd2d205` | yes | yes | no | no | no | no | no |
| 9 | `dd4546ea4f84195bdf0edfa6038a99759aea6da308a264b05d40000e07d2e682` | yes | yes | no | no | no | no | no |
| 12 | `9dc1a7b903b69ad449ac7586fa1536d4a075d28f5d9dec2fccac3d6a59027d6e` | yes | yes | no | no | no | no | no |
| 16 | `2e101bfc68d845c2015b6ef4a031245ab2eb61a99b0286fc04621135d4676a25` | yes | yes | no | no | no | no | no |
| 17 | `5d106483e6a0e272a775c0ac2aefa032deff1954f0269d8095423a752189f7ca` | yes | yes | no | no | no | no | no |
| 18 | `138510a40a4cd37d08ad928b4947f3a75f62021919c583b4773467902be05a86` | yes | yes | no | no | no | no | no |
| 19 | `88fdec3878f14f421bca4d5eda8937e69820dc2351de4cf3c5dc6da146fc0ba2` | yes | yes | no | no | no | no | no |

## Design consequence

The producer must not convert current queue rows directly into executable task
chains. A `review/admission` stage must enrich a raw brief into the required
envelope, or reject/defer it with a reason. This preserves the ideas queue as
raw material while ensuring only recoverable, testable work enters the task
ledger.

The strongest canary candidate is queue line 19, chaos engineering, because the
repository already has retry paths and bounded tests. Its eventual admission
still requires a named retry subject, predicted failure/recovery behavior,
exact test command, expected artifact, and feedback rule. Selection here does
not start the literature canary before its chain step becomes current.
