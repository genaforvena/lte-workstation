# Employer screening — А7-ТЕХНОЛОГИИ — 2026-09-07

Source: live HH chat `5598829440`, vacancy `136250383`, observed by
`mesh-hh-drive --peek` at 12:08 UTC. The employer requested a numbered answer:

1. full name;
2. desired net salary;
3. readiness for 4 days in office / 1 day remote;
4. total DevOps experience;
5. concrete Kubernetes work, plus an up-to-date PDF CV.

## Known without asking

- Full name: Илья Мозеров (`~/.mesh/job/cv-source-2026-08-14.md`).
- Compensation: public ask 500,000 ₽ net; confirmed acceptable floor 400,000 ₽ net
  (`~/.mesh/job/answers-2026-08-14.md`).
- Office/remote format: operator answered “вообще как угодно”; 4/1 is therefore
  acceptable and does not require a new question.
- PDF: `~/.mesh/job/Мозеров_Илья_CV.pdf` exists and is non-empty.
- The CV supports Kubernetes/infrastructure work at ArtNight and SoundCloud and
  Terraform/Yandex Cloud work at Foxible. It does not specify the exact Kubernetes
  operations requested by the employer.

## Machine-side open item

The operator was asked once, over TG, for only the missing Kubernetes task details.
No salary or office question is pending. Until that fact arrives, do not invent
cluster, upgrade, manifest, or Helm experience and do not send a misleading answer.

This is screening, not a confirmed interview: no calendar row or Telegram interview
alert is warranted yet.

## Delivery verification

The response and PDF were read back in the HH thread at 15:16 MSK. The first send
was duplicated because two `mesh-hh-drive.py` processes had been started at the same
time (PIDs `133885` and `134099`) and consumed the shared command stream. The orphan
`133885` was terminated; the pidfile owner `134099` remains. Both production and repo
wrappers now serialize the pidfile/census check-and-launch transaction with
`$HOME/.mesh/job/hh-drive.start.lock`.

Verification: `bash -n` passed for both wrappers; two concurrent `--start` calls both
returned the same existing PID; the live process census is now exactly one driver.
