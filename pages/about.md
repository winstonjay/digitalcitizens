---
layout: page
title: About
permalink: /about/
---

{{ site.description }}

**TODO:** more about?

**Sources and Github repository:**

* [`master`](https://github.com/winstonjay/digitalcitizens), for code files, jupyter notebooks and other supporting materials.
* [`gh-pages`](https://github.com/winstonjay/digitalcitizens/tree/gh-pages), for blog content files.

I havent left an email address but if your would like to get in touch, notice any mistakes or anything like that feel free to [open a issue via github](https://github.com/winstonjay/digitalcitizens/issues/new).

**Archive of this page**

On a bit of a side-line I have been using this page to prototype creating version archives of GitHub pages. Below are all the different version histories that were created. Now, as some of the content is more dynamically generated, it is the same across multiple versions. For instance, the archive table once it appears in the template, will always be the current archive.

<table>
    <tr>
        <th>Created</th>
        <th>commit.file</th>
        <th>Commit comment</th>
    </tr>
    {% for entry in site.data.history %}
    <tr>
        <td>{{ entry.created }}</td>
        <td><a href="{{ site.baseurl }}/{{ entry.src }}">{{ entry.id }}</a></td>
        <td>{{ entry.comment }}</td>
    </tr>
    {% endfor %}
</table>