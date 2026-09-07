# Job autonomy audit — 2026-09-07

The live job window is wired: `mesh-home:11` is the `job-` window with a refreshing data pane and
the job mind pane; the cron reflexes cover scanning, applying, mail/chat reading, replies, calendar
reminders, confirmation promotion, and Telegram delivery.

## Verified now

- Default HH driver and named Getmatch driver are alive.
- `mesh-job-confirm --json` completes successfully and returns `[]`; its prior lock-context failure
  is covered by `tests/test-job-hh-serialization.sh` and the current lock implementation lets body
  exceptions escape without yielding twice.
- `mesh-job-cal --agenda --json` is empty, and the durable schedule has no current confirmed row.
  Therefore no interview Telegram alert is sent until date/time, participants, and link/place are
  all present.
- The pane now distinguishes HH's employer-side `interview` status from durable calendar
  confirmations: `CONFIRMED INTERVIEWS (durable calendar, not HH status): 0`.
- `mesh-dash --test-fast` passes; apply, serialization, interview-confirm, Python compile, and
  diff checks pass in the current lane.

The existing board still contains employer-side HH interview-stage rows, but their appointment
offers are cancelled or historical. They are not presented as confirmed meetings, and no operator
question was needed because the current state is inferable from the durable calendar.

The mail/action tape was also drained during the audit: the generic employer notice `18189`, the
explicit rejection `18180`, and the unjoinable Linux question `18179` were discharged with explicit
machine-side reasons. The action tape now reports no `open` rows; no question was sent to the
operator.

There remain 57 historical `over` records in the tape. They are not open current work; most lack
company identity and therefore cannot be safely joined to an HH thread. The pane continues to show
that degraded count rather than hiding it, while fresh actionable rows are handled by the scheduled
mail/reply reflexes.

The Getmatch apply path was exercised again. A repeated stale marker bug was found and fixed: cron
processes now namespace driver markers with PID and process-start nanoseconds, so `--wait` cannot
reuse a marker from an earlier run. Rows with a prior timeout or unconfirmed submission are also
excluded from autonomous retry; they remain available for exact-ID reconciliation. A fresh top-1
attempt then selected vacancy `35169`; the live applications page did not contain that ID, so it
remains unconfirmed and was not marked sent. No duplicate retry is scheduled for it.

The installed Getmatch cron reflex now invokes `--top 1` at 08:19 and 14:19. This bounds each
autonomous browser submission to one vacancy, prevents an unlimited batch from monopolising the
shared driver/confirmation lock, and leaves the next eligible vacancy for the next cycle.

An additional bounded run selected Sber vacancy `35405` (Senior Go-разработчик, GigaChat). The
form click completed, but the fresh applications page did not contain exact ID `35405`; it remains
unconfirmed, with no `sent` artifact and no automatic retry.

The reflex source header now declares `reflex-args: --top 1`. An autowire pass had reintroduced a
second unlimited crontab line from the old `(none)` declaration; that duplicate was removed, and
the installed crontab now has exactly one Getmatch apply entry.

The live reply cycle answered Valletta.Software and proposed Tue 08.09 at 12:00/13:00/14:00/15:00
MSK. A confirm-path bug then surfaced: HH's chat page includes unrelated sidebar rejections, which
were being mistaken for Valletta's rejection and cancelling the proposed calendar row. The parser
now bounds rejection/confirmation extraction to the active vacancy segment; cron-style confirm was
verified under `PATH=/usr/bin:/bin`, and the Valletta row remains durably `proposed`. No interview
Telegram alert is sent until the employer accepts a slot and supplies a link or place plus
participants.

At 14:38 UTC the lane audit found autowire had reintroduced the obsolete unlimited Getmatch
crontab entry. It was removed again; verification shows exactly one apply entry and it is
`--top 1`. The employer-mail poll found no new live-lane messages, and the only calendar item
remains Valletta's unconfirmed proposal; no interview alert was sent.

The next bounded apply checks selected Getmatch IDs `35521` and `35022`; both were verified
archived before any form click. They are now machine-owned `dropped` records, not `needs-human`.
The apply reflex was changed and installed in parity so archived vacancies and vacancies without a
verified profile letter are classified as `dropped`; the regression self-test passes in both repo
and production copies. Existing board cleanup converted 660 historical rows with the exact
"письмо не собралось" reason to `dropped`; 52 rows with genuine questionnaire/form uncertainty
remain machine-owned exceptions and are not presented as operator tasks.

The recurring wiring drift was traced to the node-local desired set `~/.mesh/reflexes.cron`, which
still held the obsolete unlimited line; `mesh-reflexes --apply` was faithfully reinstalling it.
That desired entry is now corrected to `--top 1`, the live crontab was reconciled, and
`mesh-reflexes --check` reports all desired reflexes present with exactly one apply entry.

The 14:46 live mail/reply/confirm pass found no invitation or employer acceptance. A fresh
Getmatch scan added no rows; bounded attempts for IDs `35076` (Сбер) and `35618` (X5 Tech) both
reached the click path but failed exact-ID reconciliation in `/applications`. They remain seen
with the retry guard's `отправка НЕ подтверждена` note, so the lane will not click either again.
The durable calendar still contains only Valletta's proposed, not confirmed, slots.

The fresh HH scan completed a 31-query pass and appended 192 new rows. The Getmatch selector was
then corrected to rank fresh scan dates before fit ties, preventing stale archived rows from
monopolising the bounded submitter; the regression test and installed-copy hash both pass. Its
next selected fresh vacancy was VK `36109` (Руководитель разработки [Remote]); the click reached
the form, but exact-ID reconciliation again found no matching application. It remains
unconfirmed and retry-blocked; no false `sent` artifact was created.

An audit of the Getmatch applications DOM then found the exact href for `36113` despite its
body-text verifier false negative. The verifier now captures application vacancy hrefs and accepts
only an exact numeric ID (title-only text and neighbouring IDs are regression-tested as failures).
Repo and production copies match; `36113` was reconciled to `sent` with a durable ledger entry and
sent-letter artifact. IDs `35076`, `35618`, and `36109` were absent from the live href set and
remain unconfirmed/retry-blocked.

The next Getmatch attempt exposed two independent verifier/form defects. The application form
showed a city suggestion after typing `Нижний Новгород`, but left its hidden `locationId` empty;
the submit therefore stayed on the vacancy page. The form command now selects the suggestion, with
a regression check for the resulting command. A live diagnostic confirmed that selection populates
`locationId`.

The live applications links use the canonical `/vacancies/<id>-<slug>?...` form. The exact-ID
verifier previously accepted only an ID followed by a separator/query, so it rejected a real
application such as `36085-vedushchii-go-razrabotchik`. The verifier now accepts the slug form while
still rejecting neighbouring IDs; both source and installed smoke-tests pass. A bounded run then
confirmed VK vacancy `36085` in the live applications list (45 total applications, waiting for
employer review), and it was reconciled to the durable sent ledger/artifact. No interview was
created by this application; the calendar remains unchanged.

The repaired submitter was exercised again against Sber vacancy `36063` (Middle/Senior Python
разработчик, Лаборатория данных). The city-suggestion selection and slug-aware exact-ID verifier
both held in the live browser: the application was confirmed in Getmatch's own list and written to
the sent ledger and artifact. This is the first post-fix bounded run to complete end-to-end;
`mesh-job-confirm --json` still returns no confirmed interview, and the durable calendar remains
unchanged.

The following bounded run selected VK vacancy `36033` (Team Lead Go [Remote]). It completed the
same repaired path end-to-end: city selection, form submission, exact slug-aware ID verification,
and durable board/ledger/sent-artifact recording. The calendar and interview-confirmation result
were unchanged.
