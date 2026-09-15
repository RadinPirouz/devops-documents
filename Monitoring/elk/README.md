# Elasticsearch Documentation

Unified guide covering the video course (lessons 0–21) plus stack overview notes.

Send requests from **Kibana Dev Tools** (or `curl`) using:

```http
<METHOD> <path>
{
  ...body...
}
```

[← Back to Monitoring](../README.md)

## Course (video series)

| # | Video | Doc |
| - | ----- | --- |
| 0 | intro | [00-Intro.md](00-Intro.md) |
| 1 | architecture | [01-Architecture.md](01-Architecture.md) |
| 2 | index | [02-Index.md](02-Index.md) |
| 3 | mget | [03-Mget.md](03-Mget.md) |
| 4 | search | [04-Search.md](04-Search.md) |
| 5 | query | [05-Query.md](05-Query.md) |
| 6 | compound | [06-Compound.md](06-Compound.md) |
| 7 | aggregation | [07-Aggregation.md](07-Aggregation.md) |
| 8 | relevance | [08-Relevance.md](08-Relevance.md) |
| 9 | mapping | [09-Mapping.md](09-Mapping.md) |
| 10 | runtime fields | [10-Runtime-Fields.md](10-Runtime-Fields.md) |
| 11 | update | [11-Update.md](11-Update.md) |
| 12 | settings | [12-Settings.md](12-Settings.md) |
| 13 | alias | [13-Alias.md](13-Alias.md) |
| 14 | index template | [14-Index-Template.md](14-Index-Template.md) |
| 15 | split / shrink | [15-Split-Shrink.md](15-Split-Shrink.md) |
| 16 | text analysis | [16-Text-Analysis.md](16-Text-Analysis.md) |
| 17 | tokenizer | [17-Tokenizer.md](17-Tokenizer.md) |
| 18 | specify analyzer | [18-Specify-Analyzer.md](18-Specify-Analyzer.md) |
| 19 | persian | [19-Persian.md](19-Persian.md) |
| 20 | elastic-py | [20-Elastic-Py.md](20-Elastic-Py.md) |
| 21 | django-elastic | [21-Django-Elastic.md](21-Django-Elastic.md) |

## Supplementary

| Doc | Topic |
| --- | ----- |
| [Stack-Overview.md](Stack-Overview.md) | ELK stack (Elasticsearch, Logstash, Kibana, Beats) |
| [Node-Types.md](Node-Types.md) | Master, data (hot/warm/cold), coordinating, ingest, ML |

## Suggested path

```
Intro → Architecture → Index → Documents (CRUD / mget)
  → Search → Query DSL → Compound → Aggregations → Relevance
  → Mapping → Runtime fields → Update → Settings
  → Alias → Templates → Split/Shrink
  → Analysis → Tokenizer → Analyzers → Persian
  → Python client → Django
```
