# LibDOM

LibDOM is a Python library that abstracts HTML tags, allowing you to create dynamic HTML documents in a simple and programmatic way. With LibDOM, you can generate HTML structures entirely in Python, bringing clarity and flexibility to web development.

## Key Features

- **Complete Abstraction**: Supports all HTML tags (non-obsolete).
- **Flexibility**: Ideal for creating dynamic web pages that require frequent updates.
- **Productivity**: Reduces repetitive code, simplifies maintenance, and accelerates development.

## Example

```py
from libdom.Elements import *
from libdom.Styles import *

html = Html(
    Head(
        Style({
            "body": {
                Margin: "0",
                Padding: "0",
                Display: "flex",
                JustifyContent: "center",
                AlignItems: "center"
            },
            
            ".div": {
                Border: "1px solid black",
                BackgroundColor: "red",
                "&:hover": {
                    BackgroundColor: "blue"
                }
            }
        })
    ),
    Body(
        Div(
            P("Hello World"),
            **{ Div.Attribute.Class: "div" }
        )
    )
)

print(html)

#<html>
#    <head>
#        <style>
#            body {
#                margin: 0;
#                padding: 0;
#                display: flex;
#                justify-content: center;
#                align-items: center;
#            }
#            #div {
#                border: 1px solid black;
#                background-color: red;
#                &:hover {
#                    background-color: blue;
#                }
#            }
#        </style>
#    </head>
#    <body>
#        <div class="div">
#            <p>
#                Hello World
#            </p>
#        </div>
#    </body>
#</html>
```