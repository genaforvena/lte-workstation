# HH incoming follow-up 2 — 2026-09-07

The Finbridge and Т Плюс conversations continued with screening questions. The lane answered and read back each response:

- Finbridge (`5602124977`, Руководитель web разработки): Saga/CQRS, MySQL/MongoDB, and AI-agent process integration. The lane did not invent named Saga/CQRS or MongoDB work; it stated the confirmed MySQL/general stack and PostgreSQL/Redis/Kafka/ClickHouse production contour, and described the two-year internal multi-agent workflow with artifact-based verification.
- Т Плюс (`5601998996`, Руководитель отдела разработки): Scrum/Kanban/Agile, Product Owner/business interaction, and end-to-end development ownership. The lane did not claim formal Scrum/Kanban implementation; it described confirmed iterative delivery, CI/CD, observability, team leadership, and end-to-end DSP/production ownership.

Both threads also received the known standard profile facts (Нижний Новгород, open remote/hybrid/office formats, flexible schedule, 500,000 ₽ net expectation, neutral recommendation wording). No interview date, meeting link, place, or participant list was present, so no calendar row or Telegram interview alert was created.

Readback evidence is in `~/.mesh/job/hh-drive.log`; message drafts are under `~/.mesh/job/letters/` with the `20260907` names.

During the final live check, the installed `mesh-job-confirm` wrapper had lost its repository-path
bootstrap and failed with `ModuleNotFoundError`. Both repo and installed wrappers were repaired,
and a clean-directory wrapper regression was added; repo self-test, both wrappers, live confirm, and
calendar agenda checks now pass.

The same verification pass found a stale getmatch daemon command queue from an earlier timed-out
batch. The getmatch profile was stopped and restarted, clearing that queue; its live applications
page then loaded as authenticated and showed 44 existing applications. `mesh-job-apply-getmatch
--top 0 --json` completed without submission clicks. A new auth-preflight now starts the named
profile if needed, requires `/applications` to be the returned page, and bounds driver calls with
process-group timeouts; failed or logged-out preflight returns `n/a` before any irreversible click.
The profile was also reproduced as stable across exec-session boundaries when launched in a
detached session; preflight now starts it in its own session group for the same lifecycle guarantee.

The subsequent live HH read found one generic acknowledgement in СМИТ (`5602210353`): “Рассмотрим
ваше резюме…”, with no question, interview details, or requested action. No reply was sent. Email
polling found only employer rejections and non-job mail; no new employer question or interview was
present.

Getmatch reconciliation by exact vacancy ID found two earlier unknown-result submissions in the
live `/applications` page: `35396` Principal Tech Lead, домен Retail and `34903` Team Lead MLOps
Engineer. Those two board rows are now durably `sent` with reconciliation artifacts under
`~/.mesh/job/sent/`. The remaining unknown-result rows were not promoted because the live page did
not contain their exact IDs; they remain unconfirmed and are protected by the preflight before any
 future retry.

The next real apply attempt selected GetMatch vacancy `35400` (Senior Go Platform, Sber). Its
read-only vacancy preflight found `Вакансия в архиве`; no application form was submitted and the
board records the machine-side result as archived rather than a false sent state.

The following attempt selected VK vacancy `35503` (Senior Go developer, ML platform). The live page
was open, the form was filled, and the submit control was reached. The post-submit page reported
44 applications, but exact-ID reconciliation found no `/vacancies/35503` link. It therefore remains
`seen` with sending unconfirmed; no `sent` artifact was created and no retry was inferred. The
GetMatch submitter was corrected to use the driver's raw-tail selector syntax for the city field
(`input[placeholder^='Укажите']`), and both self-tests pass.

Current interview metric remains zero confirmed interviews: `mesh-job-cal --agenda --json` and
`mesh-job-confirm --json` both return `[]`, so there is no interview alert to send in the required
date/time/link format.
