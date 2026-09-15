# 02 — Index

Create indices, add / read / delete documents, count, and list indices.

[← Architecture](./01-Architecture.md) · [ELK index](./README.md) · [Next: mget →](./03-Mget.md)

---

## Create an index

Empty index (settings and mapping inferred later as you index):

```http
PUT /users
```

Inspect it:

```http
GET /users
```

List all indices:

```http
GET /_cat/indices?v=true
```

---

## Index a document (with ID)

`PUT` with an explicit `_id`:

```http
PUT /users/_doc/1
{
  "name": "radin",
  "age": 20
}
```

Read it back:

```http
GET /users/_doc/1
```

Response includes `_index`, `_id`, `_version`, and `_source` (your JSON).

---

## Index a document (auto ID)

`POST` without an id — Elasticsearch generates one:

```http
POST /users/_doc/
{
  "name": "radin",
  "age": 20
}
```

Then fetch with the returned id, for example:

```http
GET /users/_doc/ReqkkKABRZd1ul1F3jij
```

---

## Delete a document

```http
DELETE /users/_doc/1
```

---

## Count documents

All docs in the index, or with a simple query string:

```http
GET /users/_count
```

```http
GET /users/_count?q=name:radin
```

---

## Bulk API

Index many documents in one request. Each action line is followed by a source line (NDJSON). In Dev Tools you can use `POST _bulk` with pairs of lines:

```http
POST _bulk
{"index":{"_index":"books","_id":"1"}}
{"title":"Core Java Volume I – Fundamentals","author":"Cay S. Horstmann","edition":11,"synopsis":"Java reference book that offers a detailed explanation of various features of Core Java, including exception handling, interfaces, and lambda expressions.","amazon_rating":4.6,"release_date":"2018-08-27","tags":["Programming Languages, Java Programming"]}
{"index":{"_index":"books","_id":"2"}}
{"title":"Effective Java","author":"Joshua Bloch","edition":3,"synopsis":"A must-have book for every Java programmer and Java aspirant.","amazon_rating":4.7,"release_date":"2017-12-27","tags":["Object Oriented Software Design"]}
{"index":{"_index":"books","_id":"3"}}
{"title":"Java: A Beginner’s Guide","author":"Herbert Schildt","edition":8,"synopsis":"One of the most comprehensive books for learning Java.","amazon_rating":4.2,"release_date":"2018-11-20","tags":["Software Design & Engineering","Internet & Web"]}
{"index":{"_index":"books","_id":"4"}}
{"title":"Java - The Complete Reference","author":"Herbert Schildt","edition":11,"synopsis":"Convenient Java reference book examining essential portions of the Java API library.","amazon_rating":4.4,"release_date":"2019-03-19","tags":["Software Design & Engineering","Internet & Web"]}
{"index":{"_index":"books","_id":"5"}}
{"title":"Head First Java","author":"Kathy Sierra and Bert Bates","edition":2,"synopsis":"Simplicity and real-life analogies for Java concepts.","amazon_rating":4.3,"release_date":"2005-02-18","tags":["IT Certification Exams","Object-Oriented Software Design"]}
{"index":{"_index":"books","_id":"6"}}
{"title":"Java Concurrency in Practice","author":"Brian Goetz","edition":1,"synopsis":"Concurrency and multithreading for Java.","amazon_rating":4.3,"release_date":"2006-05-09","tags":["Computer Science Books","Java Programming"]}
{"index":{"_index":"books","_id":"7"}}
{"title":"Test-Driven: TDD and Acceptance TDD for Java Developers","author":"Lasse Koskela","edition":1,"synopsis":"Automation testing and TDD for Java.","amazon_rating":4.1,"release_date":"2007-10-22","tags":["Software Architecture","Java Programming"]}
{"index":{"_index":"books","_id":"8"}}
{"title":"Head First Object-Oriented Analysis Design","author":"Brett D. McLaughlin","edition":1,"synopsis":"OOAD in the Head First style.","amazon_rating":3.9,"release_date":"2014-04-29","tags":["Introductory & Beginning Programming"]}
{"index":{"_index":"books","_id":"9"}}
{"title":"Java Performance: The Definite Guide","author":"Scott Oaks","edition":1,"synopsis":"GC, JVM, and performance tuning.","amazon_rating":4.1,"release_date":"2014-03-04","tags":["Design Pattern Programming"]}
{"index":{"_index":"books","_id":"10"}}
{"title":"Head First Design Patterns","author":"Eric Freeman & Elisabeth Robson","edition":10,"synopsis":"Design patterns with a Java focus.","amazon_rating":4.5,"release_date":"2014-03-04","tags":["Design Pattern Programming"]}
```

Other bulk actions: `create`, `update`, `delete` (delete needs only the action line).

---

## Delete an index

```http
DELETE /users
```

---

## Summary

| Goal | Request |
| --- | --- |
| Create index | `PUT /users` |
| Index with id | `PUT /users/_doc/1` + body |
| Index auto id | `POST /users/_doc/` + body |
| Get document | `GET /users/_doc/1` |
| Delete document | `DELETE /users/_doc/1` |
| Count | `GET /users/_count` |
| Bulk load | `POST _bulk` (NDJSON) |
| List indices | `GET /_cat/indices?v=true` |
