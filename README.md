html2less.py
=============

html2less.py takes a HTML5 document and outputs nested rulesets (compatible with [LESS](http://lesscss.org/)) kickstarting the work on a CSS stylesheet.

What it does?
-------------

```
./html2less.py --help

Usage: html2less.py [options] [input files]
This program will read from stdin if no input files are specified.

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -d DELIMITER, --delimiter=DELIMITER
                        Delimiter: tabs or spaces? Default: spaces
  -c, --clean           Give me clean rulesets (no comments)
```

How it works?
-------------

Sample HTML5 document:

```
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>Sample HTML5 Document</title>
</head>
<body>
    <div id="container">
        <header>
            <h1>Sample HTML5 Structure</h1>
            <nav class="navigation">
                <ul>
                    <li><a href="#">Home</a></li>
                    <li><a href="#">About</a></li>
                </ul>
            </nav>
        </header>
        <section class="page-content">
            <hgroup>
                <h1>Main Section</h1>
                <h2>This is a sample HTML5 Page</h2>
            </hgroup>
            <article>
                <p>This is the content for the first article</p>
            </article>
        </section>
        <footer class="page-footer">
            <p>This is the Footer</p>
        </footer>
    </div>
</body>
</html>
```

Let's extract CSS rulesets from the document:

```
./html2less.py test.html
#container {
  /* enter your CSS here... */
  header {
    /* enter your CSS here... */
    h1 {
      /* enter your CSS here... */
    }
    .navigation {
      /* enter your CSS here... */
      ul {
        /* enter your CSS here... */
        li {
          /* enter your CSS here... */
          a {
            /* enter your CSS here... */
          }
        }
        li {
          /* enter your CSS here... */
          a {
            /* enter your CSS here... */
          }
        }
      }
    }
  }
  .page-content {
    /* enter your CSS here... */
    hgroup {
      /* enter your CSS here... */
      h1 {
        /* enter your CSS here... */
      }
      h2 {
        /* enter your CSS here... */
      }
    }
    article {
      /* enter your CSS here... */
      p {
        /* enter your CSS here... */
      }
    }
  }
  .page-footer {
    /* enter your CSS here... */
    p {
      /* enter your CSS here... */
    }
  }
}
```

Dependencies
------------

This script depends on [lxml](http://pypi.python.org/pypi/lxml).