# HeadHunter через Note 3 — проверка операторского напоминания

Дата: 2026-09-08

## Наблюдения

- `adb devices -l` видит `4d00553d61ab90b7` как `device`, модель `SM_N900`.
- На Note 3 присутствуют `com.android.chrome`, `com.sec.android.app.sbrowser` и
  `com.google.android.webview`.
- `adb -s 4d00553d61ab90b7 shell am start -a android.intent.action.VIEW -d https://hh.ru`
  завершился с `rc=0` и создал Android `ResolverActivity`. Значит, ADB-доставка URL до
  браузерного слоя работает; конкретный браузер пока не выбран явно.

## Уже существующая обвязка

Установлен `/home/mesh-home/.local/bin/mesh-hh-drive` (ссылка на `scripts/mesh-hh-drive`).
В живом `~/.mesh/reflexes.cron` присутствуют рефлексы HeadHunter/job lane:

- `mesh-job-scan`, `mesh-job-scan-li`, `mesh-job-scan-ashby`, `mesh-job-scan-getmatch`;
- `mesh-job-track`, `mesh-job-apply`, `mesh-job-apply-getmatch`;
- `mesh-job-reply`, `mesh-job-chatwatch`.

## Повторная проверка — 19:48 UTC

- URL `https://hh.ru` открыт на Note 3 явным компонентом Chrome.
- Android создал активный `com.android.chrome.document.DocumentActivity` для этого URL.
- Снимок экрана сохранён как [operator-headhunter-note3-20260908.png](operator-headhunter-note3-20260908.png).

## Ограничение проверки

Команда `cmd package` отсутствует в Android 5.0 на Note 3, поэтому выбор Chrome через
`resolve-activity` этой командой не подтвердился. Следующий точный шаг — открыть URL
явным компонентом установленного браузера или через существующий `mesh-hh-drive`, затем
снять readback текущего URL/экрана. Явный запуск Chrome и снимок выполнены выше.
