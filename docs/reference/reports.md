# Reports

HTML report generation for parsed Dota 2 matches.

Use `gem.reports.build_html_report()` when you want the HTML string, or
`gem.reports.write_html_report()` when writing a standalone report file. Map
images and downloaded icon caches are optional local assets; pass them through
`ReportAssets` when available.

---

## Generated API

## `gem.reports.assets.ReportAssets`

### `ReportAssets`

```python
class ReportAssets
```

Optional local assets used to enrich generated HTML reports.

Source: [src/gem/reports/assets.py:12](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/reports/assets.py#L12)

#### Dataclass fields

| Name | Type | Default |
|---|---|---|
| `map_image` | `str | Path | None` | `None` |
| `hero_icon_dir` | `str | Path | None` | `None` |
| `item_icon_dir` | `str | Path | None` | `None` |

## `gem.reports.builder.ReportOptions`

### `ReportOptions`

```python
class ReportOptions
```

Rendering options for HTML match reports.

Source: [src/gem/reports/builder.py:115](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/reports/builder.py#L115)

#### Dataclass fields

| Name | Type | Default |
|---|---|---|
| `title` | `str` | `'Dota 2 Match Report'` |
| `include_movement` | `bool` | `True` |

## `gem.reports.builder.build_html_report`

### `build_html_report`

```python
def build_html_report(match: ParsedMatch, *, assets: ReportAssets | None = None, options: ReportOptions | None = None, map_b64: str | None = None) -> str
```

Assemble the complete self-contained multi-tab HTML report.

Source: [src/gem/reports/builder.py:284](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/reports/builder.py#L284)

## `gem.reports.builder.write_html_report`

### `write_html_report`

```python
def write_html_report(match: ParsedMatch, output_path: str | Path, *, assets: ReportAssets | None = None, options: ReportOptions | None = None, map_b64: str | None = None) -> Path
```

Write a self-contained HTML report and return the written path.

Source: [src/gem/reports/builder.py:516](https://github.com/whanyu1212/gem-dota/blob/main/src/gem/reports/builder.py#L516)
