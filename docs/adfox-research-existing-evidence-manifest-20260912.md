# AdFox existing-evidence integrity manifest — 2026-09-12

Scope: read-only review of the 20 existing paired-source JSONL files covering the two date buckets in the historical study, their public-data counterparts, the derived AdFox and vocabulary JSON summaries, the AdFox report, and the current capture/parser code. The source rows contain private browsing and request data. This manifest publishes no row values, URLs, hostnames, bidder names, profile identifiers, placement/campaign identifiers, or query values. No traffic was collected and no file in `self-adint` was changed.

Aliases D01–D20 and P01–P20 follow the same stable lexical order of the 20 source filenames in the private `data/` and public `public-data/` sets. Original filenames are withheld. Row counts below are parseable JSON records; the public set additionally contains 319 nonblank lines that are not valid JSON and were excluded from those counts.

## Inventory and digests

| Alias | Parseable rows | Request rows | Private SHA-256 | Public SHA-256 |
|---|---:|---:|---|---|
| 01 | 1,047 | 1,033 | `1ecf156450b8210c370de0450c49f04972f410d0b6dc5fe532bad39c57d828fa` | `43026774d124cf21c9d3b2b73b3b45ce8600d9c6b0923d47688005f9c0c86867` |
| 02 | 72 | 62 | `995df89d4bdd0557425e9ac2551392f56db64e8b59340f87e7d4ac40882ec004` | `63decf95c5576c7f6cffbcfd3f663f714dd6290fae48e8f995c0759b0feb5744` |
| 03 | 3,510 | 3,454 | `5b10e0f9113d8621a4e15ec03ac819f8af87c3277b48a6435af31da320525435` | `e5cde27f6561706c20d6f1d2869f53485c7a35ad752ce9089250aa7395230e99` |
| 04 | 1,488 | 1,432 | `333363fd6581229ebe9d06be49dfa7d29937c9a5f69302c661c41771ec18d1c3` | `0f935500a9d91ca7e51208e9be3a9811452ea65e058a351dde093901465d2120` |
| 05 | 729 | 715 | `bb549c54048112224b5e5fc4cfcdbf43e90a6f5ebdc5a9d389ee884b172a1f22` | `104742b409c37ad9e4fed8012b6818c34cb195fa07bbed652b47832a780c6596` |
| 06 | 358 | 344 | `ff3f01961de7ff338bc568c94b6b97c63dc432a3dd7233fa0f65f79a7d48994f` | `ffe3131207bea3489e999f740261501e7e623f50d173616caa23b18c0a26c72a` |
| 07 | 601 | 595 | `4797c82ab4d1a18fb89a380173caeadb83d2c1819d5ce24f3ea5dac6b7ac2b71` | `e90fc172e7a4e183455eb3bb7926a64f410d9499b731d5e957bf7e5d20d69b8d` |
| 08 | 505 | 499 | `b9311b7f8fde098c623632aa0b9981cc061cebf638bfe8eadbc11fc979c7113a` | `68f40592c92991e328d94e4a46c8495049fda60e339df6313dc29c461d0f6147` |
| 09 | 2,609 | 2,563 | `2abb6e5ef010645106d91b170a6c05d84d97a656e3a3153d2e98cbb0ea42b6ad` | `b48c8e4f957597f98059dd5ff8c6d27df23a7a1e9d9132f518d3cd8114cbdd34` |
| 10 | 1,327 | 1,279 | `e17bdf0fc19542fc7c0778378446d9134e47776feb82ccc5f70f2fee9fd109ad` | `19d05b3a0383bea777a0f8d0358a785793bcb3d8c010a9c19a385287b491e2a2` |
| 11 | 845 | 831 | `2ce0cce2a2a74787b3a9b1cb659e61aa56245ca50ae61f950b36452bf78817cd` | `b1c534e97ad28031a33aa40bd9b1e377e963dba8faeda46822b3d0a05921e5b6` |
| 12 | 1,608 | 1,594 | `1dbfdc4bf035115f79ad609821545d28a5b65bdfbf13d9b37d9033238df25b4b` | `b99f7e1a25a268f36d302b79cc6863e27d0ce28a7a71db5dc1c7b5842b972b41` |
| 13 | 979 | 961 | `cb971a005ecd7365244216df82b98994e09e4ac485ad5a94a5b8c47a0bb66ca2` | `7dcdde8dcac06b5a6c7634eb29ad40a26b86727b62d1a656d651757ccf67e055` |
| 14 | 1,266 | 1,255 | `0723c0971afa2cb6541a999e82dc54503850d92ec93034c52fb457e333b8bd83` | `2b617d88d711d77b445e5518906a4fd3fa57229c485620905948ccca826b8b25` |
| 15 | 1,455 | 1,430 | `164218bb5b793d22a4a7c2e417003c2eab61648e6fea00e2adece30152e9c525` | `1a834ad11bb972b8d740672f2d58d45d267e0bb599f8157f67542b416a7b6a88` |
| 16 | 509 | 494 | `141728550efdce14223bcf17d2e8999fc74be37bd8a92290ef8259b74deb2cee` | `6124df15cf0634ff217168961f88ba9b8dee07db1fa547505504ddd2c712ebb1` |
| 17 | 1,528 | 1,500 | `461dbb9c576e3440418df2083aa6d899df984408bfe22ab664477c80e1f1ea97` | `1befe1ecaf05100667d6b374c30d0fbf5e39185ffae1e897f358c80eb95ebd28` |
| 18 | 789 | 761 | `0f4ed3c1cc11c4ac41784ae787c02857646cc3a10818d0c28c4991f4b5ab4147` | `96ad1b0906b4e340b8c219d3e38620a948eef0d91cd599b520199b3f4eb86f58` |
| 19 | 1,632 | 1,604 | `eae6c04ba52102d85c23c90f066dbb92bacb2ad80a526b598db1b788a04c4100` | `ea1604605cdd2b5a1aee275ad6310319a8a207871514bf1e70a207be7a2f4ed0` |
| 20 | 824 | 796 | `b393b25e83186f7f206df5bdce081f881fc87e961ef793586fcf5f482eb0b17b` | `3b8254d717197b0f1f7b5116843bb06c6db2728ce69bc3e767d392ea5c430e70` |
| **Total** | **23,681** | **23,202** |  |  |

Each source row set has 479 load records and 23,202 request records. All request `load_id` values join to a load record. The public copy retains the same parseable counts but has 319 additional nonblank invalid-JSON lines. No content from those lines is reproduced here.

Derived/report/code integrity:

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| AdFox derived summary (private and public copies are byte-identical) | 4,314 | `129e08d982112eb4f69c1b4ef785c7e2cbe8dffca001c97566402472082276cd` |
| Vocabulary derived summary (private and public copies are byte-identical) | 17,036 | `cb27a7e59e0ed083e803417b77227063cb1e1c3e4fff69deb19f599241dad128` |
| Existing AdFox report | 9,019 | `3f875934394b079e6aacd67e162d1e66e06dd66b946df31160f1e9dc637282ca` |
| Current `adint-adfox-cards` parser | 16,310 | `a3d660053241f4f098c5ff58bad3095396be4e459ddc8443450a61e5a6c69abe` |
| Current `adint-hb-capture` source | 124,408 | `a5b846816a9f5e16d2e39d7d066c6e968d5268db1b128257cfb3ab81dc548d67` |

## Contract coverage

| Historical per-observation requirement | Evidence present | Assessment |
|---|---|---|
| URL | A `url` field exists on all 23,202 private request rows. `req_url_full`, `req_url_bytes`, and `req_url_truncated` exist on 11,226 only. Of the 11,976 rows lacking `req_url_full`, 5,037 have a `url` exactly at the known 500-character cap; 1,129 AdFox `getBulk` paths are in rows without `req_url_full`. | **Partial.** The public copy has only capped `url` fields; its exact full-query provenance is not retained. |
| Retrieval timestamp | Every request has relative `t_request_s`; every load has a UTC `ts`; all request rows join to a load. There is no per-request absolute retrieval timestamp field. | **Partial.** A relative time plus load anchor is available, not the requested explicit observation timestamp. |
| Query/profile conditions | Every request has `arm`, `profile_age_s`, and `run_idx`; query material is in the captured URL, whose full form is absent on 11,976 rows. `arm_note` is not copied onto the request rows. | **Partial.** Conditions can be joined or inferred for some observations, but the full query/profile condition set is not preserved per row. |
| Field names | The derived summary contains aggregate entry-field counts. The raw source contains parsed evidence fields on a subset, but no per-observation field-name manifest. | **Partial.** Aggregate names are reported; the historical per-observation contract is not met. |
| Raw-response hash | No raw-response-hash, response-hash, or response-SHA field occurs in the inspected source schema. The capture stores request data plus response time/status, not a response body. | **Absent.** Hashing the ledger file or outbound request URL would not satisfy the raw-response-hash requirement. |

## Current-code reconciliation

The current capture code preserves both a legacy `url` field capped at 500 characters and, in newer rows, a `req_url_full` field with original byte length and a truncation flag. The current AdFox parser reads `req_url_full` only. It does not fall back to `url`.

Across the 20 historical source files, there are 2,239 request rows whose captured URL contains the AdFox `getBulk` path. Only 1,110 are in `req_url_full`; the other 1,129 are on rows without it. The existing summary reports 1,110 `getBulk` requests and 1,093 with `bids=`. This matches the parser's `req_url_full`-only subset and omits the earlier date bucket, despite the report describing a two-date corpus. The omitted URLs are not safely recoverable from the shared public copy; the private rows may contain only a capped URL.

The historical report remains useful evidence that the exposed outbound request carries bidder fields on the subset it parsed. It does not satisfy the original per-observation provenance contract: the response body/hash is absent, time is relative rather than an explicit UTC observation timestamp, and the existing field report is aggregate. The audit therefore finds a material evidence gap; it does not authorize another collection. The next task owner can decide whether a bounded successor design is justified.

## Verification performed

- Parsed only local source JSONL and emitted counts, key-presence totals, byte lengths, and SHA-256 values; never emitted row values.
- Reconciled source counts against both derived JSON files and the current parser's URL-field selection.
- Read the historical ask and existing AdFox report, then inspected the capture/parser code paths for timestamp, URL truncation, and response-body handling.
- No collection command, source-data write, or edit in `/home/mesh-home/self-adint` was performed.
