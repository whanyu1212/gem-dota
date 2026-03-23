# uifontfile_format.proto

- Module: `uifontfile_format_pb2`
- Syntax: `unknown`
- Package: `(none)`
- Imports: **0**
- Messages: **3** (top-level: 2)
- Enums: **0** (top-level: 0)

## Messages

Expand any message to inspect all fields.

<details>
<summary><code>CUIFontFilePB</code> — fields: 2; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `font_file_name` | `string` | `optional` | `` |  |
| 2 | `opentype_font_data` | `bytes` | `optional` | `` |  |

</details>

<details>
<summary><code>CUIFontFilePackagePB</code> — fields: 2; oneofs: 0; nested messages: 1; nested enums: 0</summary>

- Parent: *(top-level)*
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `package_version` | `uint32` | `required` | `` |  |
| 2 | `encrypted_font_files` | `.CUIFontFilePackagePB.CUIEncryptedFontFilePB` | `repeated` | `` |  |

</details>

<details>
<summary><code>CUIFontFilePackagePB.CUIEncryptedFontFilePB</code> — fields: 1; oneofs: 0; nested messages: 0; nested enums: 0</summary>

- Parent: `CUIFontFilePackagePB`
- Oneofs: *(none)*

| Tag | Field | Type | Label | Oneof | Notes |
|---:|---|---|---|---|---|
| 1 | `encrypted_contents` | `bytes` | `optional` | `` |  |

</details>

## Enums

Expand any enum to inspect all values.

*(No enums in this proto file.)*
