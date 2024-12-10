import inspect
import textwrap
from .Attributes import GlobalAttributes

class Element:
    class Inline:
        class Attributes(GlobalAttributes):
            pass
            
        def __init__(self, *args, **kwargs):
            if "cls" in kwargs:
                kwargs["class"] = kwargs.pop("cls")
                
            self.args = args
            self.kwargs = kwargs
            self.tag_name = self.__class__.__name__.lower()
            
        def __str__(self):
            return self._render()
            
        def _render(self, indent: int = 0):
            indentation = "    " * indent
            result = f"{indentation}<{self.tag_name}{' ' if len(self.kwargs) > 0 else ''}{' '.join(f'{key}=\"{value}\"' for key, value in self.kwargs.items())}/>"
            return result
            
    class BlockLevel:
        class Attributes(GlobalAttributes):
            pass
            
        def __init__(self, *args, **kwargs):
            if "cls" in kwargs:
                kwargs["class"] = kwargs.pop("cls")
                
            self.args = args
            self.kwargs = kwargs
            self.tag_name = self.__class__.__name__.lower()
            
        def __str__(self):
            return self._render()
            
        def _render(self, indent: int = 0):
            indentation = "    " * indent
            result = f"{indentation}<{self.tag_name}{' ' if len(self.kwargs) > 0 else ''}{' '.join(f'{key}=\"{value}\"' for key, value in self.kwargs.items())}>"
            
            for arg in self.args:
                if hasattr(arg, '_render'):
                    result += "\n" + arg._render(indent + 1)
                else:
                    if callable(arg):
                        source_code = inspect.getsource(arg)
                        lines = source_code.splitlines()
                        formatted_code = textwrap.dedent("\n".join(lines[1:]))
                        result += f"\n{indentation}    {formatted_code}"
                    else:
                        result += f"\n{indentation}    {arg}"
                    
            result += f"\n{indentation}</{self.tag_name}>"
            
            return result

    class Style:
        class Attributes(GlobalAttributes):
            pass
            
        def __init__(self, styles: dict, *args, **kwargs):
            if "cls" in kwargs:
                kwargs["class"] = kwargs.pop("cls")
                
            self.args = args
            self.kwargs = kwargs
            self.styles = styles
            
        def __str__(self):
            return self._render(indent=1)
        
        def _render(self, indent=0):
            def process_styles(styles, current_indent=0):
                css_lines = []
                indentation = "    " * (current_indent + 1)
                
                for selector, properties in styles.items():
                    css_lines.append(f"{indentation}{selector} {{")
                    
                    for prop, value in properties.items():
                        if isinstance(value, dict):
                            nested_lines = process_styles(
                                {prop: value}, current_indent + 1
                            )
                            css_lines.extend(nested_lines)
                        else:
                            css_lines.append(f"{indentation}    {prop}: {value};")
                    
                    css_lines.append(f"{indentation}}}")
                
                return css_lines
            
            css_content = "\n".join(process_styles(self.styles, current_indent=indent))
            indentation = "    " * indent
            return f"{indentation}<style{' ' if len(self.kwargs) > 0 else ''}{' '.join(f'{key}=\"{value}\"' for key, value in self.kwargs.items())}>\n{css_content}\n{indentation}</style>"

class Html(Element.BlockLevel):
    """
    Represents the root (top-level element) of an HTML document, so it is also referred to as the root element. All other elements must be descendants of this element.
    """
    pass

class Base(Element.Inline):
    """
    Specifies the base URL to use for all relative URLs in a document. There can be only one such element in a document.
    """
    class Attributes(Element.Inline.Attributes):
        Href = "href"
        Target = "target"
    pass

class Head(Element.BlockLevel):
    """
    Contains machine-readable information (metadata) about the document, like its title, scripts, and style sheets.
    """
    pass

class Link(Element.Inline):
    """
    Specifies relationships between the current document and an external resource. This element is most commonly used to link to CSS but is also used to establish site icons (both "favicon" style icons and icons for the home screen and apps on mobile devices) among other things.
    """
    class Attributes(Element.Inline.Attributes):
        As = "as"
        Crossorigin = "crossorigin"
        Href = "href"
        Hreflang = "hreflang"
        Integrity = "integrity"
        Media = "media"
        Referrerpolicy = "referrerpolicy"
        Rel = "rel"
        Sizes = "sizes"
        Type = "type"
    pass

class Meta(Element.Inline):
    """
    Represents metadata that cannot be represented by other HTML meta-related elements, like <base>, <link>, <script>, <style> and <title>.
    """
    class Attributes(Element.Inline.Attributes):
        Charset = "charset"
        Content = "content"
        HttpEquiv = "http-equiv"
        Name = "name"
    pass

class Style(Element.Style):
    """Contains style information for a document or part of a document. It contains CSS, which is applied to the contents of the document containing this element."""
    class Attributes(Element.Style.Attributes):
        Media = "media"
        Scoped = "scoped"
        Type = "type"
    pass

class Title(Element.BlockLevel):
    """Defines the document's title that is shown in a browser's title bar or a page's tab. It only contains text; HTML tags within the element, if any, are also treated as plain text."""
    pass

class Body(Element.BlockLevel):
    """
    Represents the content of an HTML document. There can be only one such element in a document.
    """
    class Attributes(Element.BlockLevel.Attributes):
        Background = "background"
        Bgcolor = "bgcolor"
    pass

class Address(Element.BlockLevel):
    """
    Indicates that the enclosed HTML provides contact information for a person or people, or for an organization.
    """
    pass

class Article(Element.BlockLevel):
    """Represents a self-contained composition in a document, page, application, or site, which is intended to be independently distributable or reusable (e.g., in syndication). Examples include a forum post, a magazine or newspaper article, a blog entry, a product card, a user-submitted comment, an interactive widget or gadget, or any other independent item of content."""
    pass

class Aside(Element.BlockLevel):
    """
    Represents a portion of a document whose content is only indirectly related to the document's main content. Asides are frequently presented as sidebars or call-out boxes.
    """
    pass

class Footer(Element.BlockLevel):
    """
    Represents a footer for its nearest ancestor sectioning content or sectioning root element. A <footer> typically contains information about the author of the section, copyright data, or links to related documents.
    """
    pass

class Header(Element.BlockLevel):
    """
    Represents introductory content, typically a group of introductory or navigational aids. It may contain some heading elements but also a logo, a search form, an author name, and other elements.
    """
    pass

class H1(Element.BlockLevel):
    """
    Represent six levels of section headings. <h1> is the highest section level and <h6> is the lowest.
    """
    pass

class H2(Element.BlockLevel):
    """
    Represent six levels of section headings. <h1> is the highest section level and <h6> is the lowest.
    """
    pass

class H3(Element.BlockLevel):
    """
    Represent six levels of section headings. <h1> is the highest section level and <h6> is the lowest.
    """
    pass

class H4(Element.BlockLevel):
    """
    Represent six levels of section headings. <h1> is the highest section level and <h6> is the lowest.
    """
    pass

class H5(Element.BlockLevel):
    """
    Represent six levels of section headings. <h1> is the highest section level and <h6> is the lowest.
    """
    pass

class H6(Element.BlockLevel):
    """
    Represent six levels of section headings. <h1> is the highest section level and <h6> is the lowest.
    """
    pass

class Hgroup(Element.BlockLevel):
    """
    Represents a heading grouped with any secondary content, such as subheadings, an alternative title, or a tagline.
    """
    pass

class Main(Element.BlockLevel):
    """
    Represents the dominant content of the body of a document. The main content area consists of content that is directly related to or expands upon the central topic of a document, or the central functionality of an application.
    """
    pass

class Nav(Element.BlockLevel):
    """
    Represents a section of a page whose purpose is to provide navigation links, either within the current document or to other documents. Common examples of navigation sections are menus, tables of contents, and indexes.
    """
    pass

class Section(Element.BlockLevel):
    """
    Represents a generic standalone section of a document, which doesn't have a more specific semantic element to represent it. Sections should always have a heading, with very few exceptions.
    """
    pass

class Search(Element.BlockLevel):
    """
    Represents a part that contains a set of form controls or other content related to performing a search or filtering operation.
    """
    pass

class BlockQuote(Element.BlockLevel):
    """
    Indicates that the enclosed text is an extended quotation. Usually, this is rendered visually by indentation. A URL for the source of the quotation may be given using the cite Attributes, while a text representation of the source can be given using the <cite> element.
    """
    class Attributes(Element.BlockLevel.Attributes):
        Cite = "cite"
    pass

class Dd(Element.BlockLevel):
    """
    Provides the description, definition, or value for the preceding term (<dt>) in a description list (<dl>).
    """
    pass

class Div(Element.BlockLevel):
    """
    The generic container for flow content. It has no effect on the content or layout until styled in some way using CSS (e.g., styling is directly applied to it, or some kind of layout model like flexbox is applied to its parent element).
    """
    pass

class Dl(Element.BlockLevel):
    """
    Represents a description list. The element encloses a list of groups of terms (specified using the <dt> element) and descriptions (provided by <dd> elements). Common uses for this element are to implement a glossary or to display metadata (a list of key-value pairs).
    """
    pass

class Dt(Element.BlockLevel):
    """
    Specifies a term in a description or definition list, and as such must be used inside a <dl> element. It is usually followed by a <dd> element; however, multiple <dt> elements in a row indicate several terms that are all defined by the immediate next <dd> element.
    """
    pass

class Figcaption(Element.BlockLevel):
    """
    Represents a caption or legend describing the rest of the contents of its parent <figure> element.
    """
    pass

class Figure(Element.BlockLevel):
    """
    Represents self-contained content, potentially with an optional caption, which is specified using the <figcaption> element. The figure, its caption, and its contents are referenced as a single unit.
    """
    pass

class Hr(Element.Inline):
    """
    Represents a thematic break between paragraph-level elements: for example, a change of scene in a story, or a shift of topic within a section.
    """
    class Attributes(Element.Inline.Attributes):
        Align = "align"
        Color = "color"
    pass

class Li(Element.BlockLevel):
    """
    Represents an item in a list. It must be contained in a parent element: an ordered list (<ol>), an unordered list (<ul>), or a menu (<menu>). In menus and unordered lists, list items are usually displayed using bullet points. In ordered lists, they are usually displayed with an ascending counter on the left, such as a number or letter.
    """
    class Attributes(Element.BlockLevel.Attributes):
        Value = "value"
    pass

class Menu(Element.BlockLevel):
    """
    A semantic alternative to <ul>, but treated by browsers (and exposed through the accessibility tree) as no different than <ul>. It represents an unordered list of items (which are represented by <li> elements).
    """
    class Attributes(Element.BlockLevel.Attributes):
        Type = "type"
    pass

class Ol(Element.BlockLevel):
    """
    Represents an ordered list of items — typically rendered as a numbered list.
    """
    class Attributes(Element.BlockLevel.Attributes):
        Reversed = "reversed"
        Start = "start"
        Type = "type"
    pass

class P(Element.BlockLevel):
    """
    Represents a paragraph. Paragraphs are usually represented in visual media as blocks of text separated from adjacent blocks by blank lines andor first-line indentation, but HTML paragraphs can be any structural grouping of related content, such as images or form fields.
    """
    pass

class Pre(Element.BlockLevel):
    """
    Represents preformatted text which is to be presented exactly as written in the HTML file. The text is typically rendered using a non-proportional, or monospaced, font. Whitespace inside this element is displayed as written.
    """
    pass

class Ul(Element.BlockLevel):
    """
    Represents an unordered list of items, typically rendered as a bulleted list.
    """
    pass

class A(Element.BlockLevel):
    """
    Together with its href Attributes, creates a hyperlink to web pages, files, email addresses, locations within the current page, or anything else a URL can address.
    """
    class Attributes(Element.BlockLevel.Attributes):
        Download = "download"
        Href = "href"
        Hreflang = "hreflang"
        Media = "media"
        Ping = "ping"
        Referrerpolicy = "referrerpolicy"
        Rel = "rel"
        Shape = "shape"
        Target = "target"
    pass

class Abbr(Element.BlockLevel):
    """
    Represents an abbreviation or acronym.
    """
    pass

class B(Element.BlockLevel):
    """
    Used to draw the reader's attention to the element's contents, which are not otherwise granted special
    importance. This was formerly known as the Boldface element, and most browsers still draw the text in boldface.
    However, you should not use <b> for styling text or granting importance. If you wish to create boldface text,
    you should use the CSS font-weight property. If you wish to indicate an element is of special importance,
    you should use the strong element.
    """
    pass

class Bdi(Element.BlockLevel):
    """
    Tells the browser's bidirectional algorithm to treat the text it contains in isolation from its surrounding text.
    It's particularly useful when a website dynamically inserts some text and doesn't know the directionality of
    the text being inserted.
    """
    pass

class Bdo(Element.BlockLevel):
    """
    Overrides the current directionality of text, so that the text within is rendered in a different direction.
    """
    pass

class Br(Element.Inline):
    """
    Produces a line break in text (carriage-return). It is useful for writing a poem or an address, where the
    division of lines is significant.
    """
    pass

class Cite(Element.BlockLevel):
    """
    Used to mark up the title of a cited creative work. The reference may be in an abbreviated form according
    to context-appropriate conventions related to citation metadata.
    """
    pass

class Code(Element.BlockLevel):
    """
    Displays its contents styled in a fashion intended to indicate that the text is a short fragment of computer code.
    By default, the content text is displayed using the user agent's default monospace font.
    """
    pass

class Data(Element.BlockLevel):
    """
    Links a given piece of content with a machine-readable translation. If the content is time- or date-related,
    the <time> element must be used.
    """
    class Attributes(Element.BlockLevel.Attributes):
        Value = "value"
    pass

class Dfn(Element.BlockLevel):
    """
    Used to indicate the term being defined within the context of a definition phrase or sentence. The ancestor <p>
    element, the <dt><dd> pairing, or the nearest section ancestor of the <dfn> element, is considered to be the
    definition of the term.
    """
    pass

class Em(Element.BlockLevel):
    """
    Marks text that has stress emphasis. The <em> element can be nested, with each nesting level indicating
    a greater degree of emphasis.
    """
    pass

class I(Element.BlockLevel):
    """
    Represents a range of text that is set off from the normal text for some reason, such as idiomatic text,
    technical terms, and taxonomical designations, among others. Historically, these have been presented using
    italicized type, which is the original source of the <i> naming of this element.
    """
    pass

class Kbd(Element.BlockLevel):
    """
    Represents a span of inline text denoting textual user input from a keyboard, voice input, or any other text
    entry device. By convention, the user agent defaults to rendering the contents of a <kbd> element using its
    default monospace font, although this is not mandated by the HTML standard.
    """
    pass

class Mark(Element.BlockLevel):
    """
    Represents text which is marked or highlighted for reference or notation purposes due to the marked passage's
    relevance in the enclosing context.
    """
    pass

class Q(Element.BlockLevel):
    """
    Indicates that the enclosed text is a short inline quotation. Most modern browsers implement this by
    surrounding the text in quotation marks. This element is intended for short quotations that don't require
    paragraph breaks; for long quotations use the <blockquote> element.
    """
    class Attributes(Element.BlockLevel.Attributes):
        Cite = "cite"
    pass

class Rp(Element.BlockLevel):
    """
    Used to provide fall-back parentheses for browsers that do not support the display of ruby annotations using
    the <ruby> element. One <rp> element should enclose each of the opening and closing parentheses that wrap
    the <rt> element that contains the annotation's text.
    """
    pass

class Rt(Element.BlockLevel):
    """
    Specifies the ruby text component of a ruby annotation, which is used to provide pronunciation, translation,
    or transliteration information for East Asian typography. The <rt> element must always be contained within
    a <ruby> element.
    """
    pass

class Ruby(Element.BlockLevel):
    """
    Represents small annotations that are rendered above, below, or next to base text, usually used for showing
    the pronunciation of East Asian characters. It can also be used for annotating other kinds of text, but
    this usage is less common.
    """
    pass

class S(Element.BlockLevel):
    """
    Renders text with a strikethrough, or a line through it. Use the <s> element to represent things that
    are no longer relevant or no longer accurate. However, <s> is not appropriate when indicating document
    edits; for that, use the <del> and <ins> elements, as appropriate.
    """
    pass

class Samp(Element.BlockLevel):
    """
    Used to enclose inline text which represents sample (or quoted) output from a computer program. Its contents
    are typically rendered using the browser's default monospaced font (such as Courier or Lucida Console).
    """
    pass

class Small(Element.BlockLevel):
    """
    Represents side-comments and small print, like copyright and legal text, independent of its styled presentation.
    By default, it renders text within it one font size smaller, such as from small to x-small.
    """
    pass

class Span(Element.BlockLevel):
    """
    A generic inline container for phrasing content, which does not inherently represent anything. It can be used
    to group elements for styling purposes (using the class or id Attributess), or because they share Attributes
    values, such as lang. It should be used only when no other semantic element is appropriate. <span> is very much
    like a div element, but div is a block-level element whereas a <span> is an inline-level element.
    """
    pass

class Strong(Element.BlockLevel):
    """
    Indicates that its contents have strong importance, seriousness, or urgency. Browsers typically render the
    contents in bold type.
    """
    pass

class Sub(Element.BlockLevel):
    """
    Specifies inline text which should be displayed as subscript for solely typographical reasons. Subscripts are
    typically rendered with a lowered baseline using smaller text.
    """
    pass

class Sup(Element.BlockLevel):
    """
    Specifies inline text which is to be displayed as superscript for solely typographical reasons. Superscripts
    are usually rendered with a raised baseline using smaller text.
    """
    pass

class Time(Element.BlockLevel):
    """
    Represents a specific period in time. It may include the datetime Attributes to translate dates into
    machine-readable format, allowing for better search engine results or custom features such as reminders.
    """
    class Attributes(Element.BlockLevel.Attributes):
        Datetime = "datetime"
    pass

class U(Element.BlockLevel):
    """
    Represents a span of inline text which should be rendered in a way that indicates that it has a non-textual
    annotation. This is rendered by default as a single solid underline but may be altered using CSS.
    """
    pass

class Var(Element.BlockLevel):
    """
    Represents the name of a variable in a mathematical expression or a programming context. It's typically
    presented using an italicized version of the current typeface, although that behavior is browser-dependent.
    """
    pass

class Wbr(Element.Inline):
    """
    Represents a word break opportunity—a position within text where the browser may optionally break a line,
    though its line-breaking rules would not otherwise create a break at that location.
    """
    pass

class Area(Element.Inline):
    """
    Defines an area inside an image map that has predefined clickable areas. An image map allows geometric areas
    on an image to be associated with a hyperlink.
    """
    class Attributes(Element.Inline.Attributes):
        Alt = "alt"
        Coords = "coords"
        Download = "download"
        Href = "href"
        Media = "media"
        Ping = "ping",
        Referrerpolicy = "referrerpolicy"
        Rel = "rel"
        Shape = "shape"
        Target = "target"
    pass

class Audio(Element.Inline):
    """
    Used to embed sound content in documents. It may contain one or more audio sources, represented using the src
    Attributes or the source element: the browser will choose the most suitable one. It can also be the destination
    for streamed media, using a MediaStream.
    """
    class Attributes(Element.Inline.Attributes):
        Autoplay = "autoplay"
        Controls = "controls"
        Crossorigin = "crossorigin"
        Loop = "loop"
        Muted = "muted"
        Preload = "preload"
        Src = "src"
    pass

class Img(Element.Inline):
    """
    Embeds an image into the document.
    """
    class Attributes(Element.Inline.Attributes):
        Align = "align"
        Alt = "alt"
        Border = "border"
        Crossorigin = "crossorigin"
        Decoding = "decoding"
        Height = "height"
        Intrinsicsize = "intrinsicsize"
        Ismap = "ismap"
        Loading = "loading"
        Referrerpolicy = "referrerpolicy"
        Sizes = "sizes"
        Src = "src"
        Srcset = "srcset"
        Usemap = "usemap"
        Width = "width"
    pass

class Map(Element.BlockLevel):
    """
    Used with <area> elements to define an image map (a clickable link area).
    """
    class Attributes(Element.BlockLevel.Attributes):
        Name = "name"
    pass

class Track(Element.Inline):
    """
    Used as a child of the media elements, audio and video. It lets you specify timed text tracks (or time-based data),
    for example to automatically handle subtitles. The tracks are formatted in WebVTT format (.vtt files)—Web Video
    Text Tracks.
    """
    class Attributes(Element.Inline.Attributes):
        Default = "default"
        Kind = "kind"
        Label = "label"
        Src = "src"
        Srclang = "srclang"
    pass

class Video(Element.BlockLevel):
    """
    Embeds a media player which supports video playback into the document. You can also use <video> for audio content,
    but the audio element may provide a more appropriate user experience.
    """
    class Attributes(Element.BlockLevel.Attributes):
        Autoplay = "autoplay"
        Controls = "controls"
        Crossorigin = "crossorigin"
        Height = "height"
        Loop = "loop"
        Muted = "muted"
        Playsinline = "playsinline"
        Poster = "poster"
        Preload = "preload"
        Src = "src"
        Width = "width"
    pass

class Embed(Element.Inline):
    """
    Embeds external content at the specified point in the document. This content is provided by an external application
    or other source of interactive content such as a browser plug-in.
    """
    class Attributes(Element.Inline.Attributes):
        Height = "height"
        Src = "src"
        Type = "type"
        Width = "width"
    pass

class Fencedframe(Element.BlockLevel):
    """
    Represents a nested browsing context, like <iframe> but with more native privacy features built in.
    """
    pass

class Iframe(Element.BlockLevel):
    """
    Represents a nested browsing context, embedding another HTML page into the current one.
    """
    class Attributes(Element.BlockLevel.Attributes):
        Align = "align"
        Allow = "allow"
        Csp = "csp"
        Height = "height"
        Loading = "loading"
        Name = "name"
        Referrerpolicy = "referrerpolicy"
        Sandbox = "sandbox"
        Src = "src"
        Srcdoc = "srcdoc"
        Width = "width"

class Object(Element.BlockLevel):
    """
    Represents an external resource, which can be treated as an image, a nested browsing context, or a resource
    to be handled by a plugin.
    """
    class Attributes(Element.BlockLevel.Attributes):
        Border = "border"
        Data = "data"
        Form = "form"
        Height = "height"
        Name = "name"
        Type = "type"
        Usemap = "usemap"
        Width = "width"
    pass

class Picture(Element.BlockLevel):
    """
    Contains zero or more <source> elements and one <img> element to offer alternative versions of an image for
    different displaydevice scenarios.
    """
    pass

class Portal(Element.BlockLevel):
    """
    Enables the embedding of another HTML page into the current one to enable smoother navigation into new pages.
    """
    pass

class Source(Element.Inline):
    """
    Specifies multiple media resources for the picture, the audio element, or the video element. It is a void
    element, meaning that it has no content and does not have a closing Element. It is commonly used to offer the same
    media content in multiple file formats in order to provide compatibility with a broad range of browsers given
    their differing support for image file formats and media file formats.
    """
    class Attributes(Element.Inline.Attributes):
        Media = "media"
        Sizes = "sizes"
        Src = "src"
        Srcset = "srcset"
        Type = "type"
    pass

class Svg(Element.BlockLevel):
    """
    Container defining a new coordinate system and viewport. It is used as the outermost element of SVG documents,
    but it can also be used to embed an SVG fragment inside an SVG or HTML document.
    """
    pass

class Math(Element.BlockLevel):
    """
    The top-level element in MathML. Every valid MathML instance must be wrapped in it. In addition, you must not
    nest a second <math> element in another, but you can have an arbitrary number of other child elements in it.
    """
    pass

class Canvas(Element.BlockLevel):
    """
    Container element to use with either the canvas scripting API or the WebGL API to draw graphics and animations.
    """
    class Attributes(Element.BlockLevel.Attributes):
        Height = "height"
        Width = "width"
    pass

class Noscript(Element.BlockLevel):
    """
    Defines a section of HTML to be inserted if a script type on the page is unsupported or if scripting is
    currently turned off in the browser.
    """
    pass

class Script(Element.BlockLevel):
    """
    Used to embed executable code or data; this is typically used to embed or refer to JavaScript code.
    The <script> element can also be used with other languages, such as WebGL's GLSL shader programming language
    and JSON.
    """
    class Attributes(Element.BlockLevel.Attributes):
        Async = "async"
        Crossorigin = "crossorigin"
        Defer = "defer"
        Integrity = "integrity"
        Language = "language"
        Referrerpolicy = "referrerpolicy"
        Src = "src"
        Type = "type"
    pass

class Del(Element.BlockLevel):
    """
    Represents a range of text that has been deleted from a document. This can be used when rendering "track changes"
    or source code diff information, for example. The <ins> element can be used for the opposite purpose: to indicate
    text that has been added to the document.
    """
    class Attributes(Element.BlockLevel.Attributes):
        Cite = "cite"
        Datetime = "datetime"
    pass

class Ins(Element.BlockLevel):
    """
    Represents a range of text that has been added to a document. You can use the <del> element to similarly
    represent a range of text that has been deleted from the document.
    """
    class Attributes(Element.BlockLevel.Attributes):
        Cite = "cite"
        Datetime = "datetime"
    pass

class Caption(Element.BlockLevel):
    """
    Specifies the caption (or title) of a table.
    """
    class Attributes(Element.BlockLevel.Attributes):
        Align = "align"

class Col(Element.Inline):
    """
    Defines one or more columns in a column group represented by its implicit or explicit parent <colgroup> element.
    The <col> element is only valid as a child of a <colgroup> element that has no span Attributes defined.
    """
    class Attributes(Element.Inline.Attributes):
        Align = "align"
        Bgcolor = "bgcolor"
        Span = "span"
    pass

class ColGroup(Element.BlockLevel):
    """
    Defines a group of columns within a table.
    """
    class Attributes(Element.BlockLevel.Attributes):
        Align = "align"
        Bgcolor = "bgcolor"
        Span = "span"
    pass

class Table(Element.BlockLevel):
    """
    Represents tabular data—that is, information presented in a two-dimensional table comprised of rows and columns
    of cells containing data.
    """
    class Attributes(Element.BlockLevel.Attributes):
        Align = "align"
        Background = "background"
        Bgcolor = "bgcolor"
        Border = "border"
        Summary = "summary"
    pass

class Tbody(Element.BlockLevel):
    """
    Encapsulates a set of table rows (<tr> elements), indicating that they comprise the body of a table's (main) data.
    """
    class Attributes(Element.BlockLevel.Attributes):
        Align = "align"
        Bgcolor = "bgcolor"
    pass

class Td(Element.BlockLevel):
    """
    A child of the <tr> element, it defines a cell of a table that contains data.
    """
    class Attributes(Element.BlockLevel.Attributes):
        Align = "align"
        Background = "background"
        Bgcolor = "bgcolor"
        Colspan = "colspan"
        Headers = "headers"
        Rowspan = "rowspan"
    pass

class Tfoot(Element.BlockLevel):
    """
    Encapsulates a set of table rows (<tr> elements), indicating that they comprise the foot of a table with
    information about the table's columns. This is usually a summary of the columns, e.g., a sum of the given
    numbers in a column.
    """
    class Attributes(Element.BlockLevel.Attributes):
        Align = "align"
        Bgcolor = "bgcolor"
    pass

class Th(Element.BlockLevel):
    """
    A child of the <tr> element, it defines a cell as the header of a group of table cells. The nature of this
    group can be explicitly defined by the scope and headers Attributess.
    """
    class Attributes(Element.BlockLevel.Attributes):
        Align = "align"
        Background = "background"
        Bgcolor = "bgcolor"
        Colspan = "colspan"
        Headers = "headers"
        Rowspan = "rowspan"
        Scope = "scope"
    pass

class Thead(Element.BlockLevel):
    """
    Encapsulates a set of table rows (<tr> elements), indicating that they comprise the head of a table with
    information about the table's columns. This is usually in the form of column headers (<th> elements).
    """
    class Attributes(Element.BlockLevel.Attributes):
        Align = "align"
    pass

class Tr(Element.BlockLevel):
    """
    Defines a row of cells in a table. The row's cells can then be established using a mix of <td> (data cell)
    and <th> (header cell) elements.
    """
    class Attributes(Element.BlockLevel.Attributes):
        Align = "align"
        Bgcolor = "bgcolor"
    pass

class Button(Element.BlockLevel):
    """
    An interactive element activated by a user with a mouse, keyboard, finger, voice command, or other assistive
    technology. Once activated, it performs an action, such as submitting a form or opening a dialog.
    """
    class Attributes(Element.BlockLevel.Attributes):
        Disabled = "disabled"
        Form = "form"
        Formaction = "formaction"
        Formenctype = "formenctype"
        Formmethod = "formmethod"
        Formnovalidate = "formnovalidate"
        Formtarget = "formtarget"
        Name = "name"
        Type = "type"
        Value = "value"
    pass

class Datalist(Element.BlockLevel):
    """
    Contains a set of <option> elements that represent the permissible or recommended options available to choose
    from within other controls.
    """
    pass

class Fieldset(Element.BlockLevel):
    """
    Used to group several controls as well as labels (<label>) within a web form.
    """
    class Attributes(Element.BlockLevel.Attributes):
        Disabled = "disabled"
        Form = "form"
        Name = "name"
    pass

class Form(Element.BlockLevel):
    """
    Represents a document section containing interactive controls for submitting information.
    """
    class Attributes(Element.BlockLevel.Attributes):
        Accept = "accept"
        AcceptCharset = "accept-charset"
        Action = "action"
        Autocomplete = "autocomplete"
        Enctype = "enctype"
        Method = "method"
        Name = "name"
        Novalidate = "novalidate"
        Target = "target"

class Input(Element.Inline):
    """
    Used to create interactive controls for web-based forms to accept data from the user; a wide variety of types
    of input data and control widgets are available, depending on the device and user agent. The <input> element
    is one of the most powerful and complex in all of HTML due to the sheer number of combinations of input types
    and Attributess.
    """
    class Attributes(Element.Inline.Attributes):
        Accept = "accept"
        Alt = "alt"
        Autocomplete = "autocomplete"
        Capture = "capture"
        Checked = "checked"
        Dirname = "dirname"
        Disabled = "disabled"
        Form = "form"
        Formaction = "formaction"
        Formenctype = "formenctype"
        Formmethod = "formmethod"
        Formnovalidate = "formnovalidate"
        Formtarget = "formtarget"
        Height = "height"
        List = "list"
        Max = "max"
        Maxlength = "maxlength"
        Minlength = "minlength"
        Min = "min"
        Multiple = "multiple"
        Name = "name"
        Pattern = "pattern"
        Placeholder = "placeholder"
        Readonly = "readonly"
        Required = "required"
        Size = "size"
        Src = "src"
        Step = "step"
        Type = "type"
        Usemap = "usemap"
        Value = "value"
        Width = "width"

class Label(Element.BlockLevel):
    """
    Represents a caption for an item in a user interface.
    """
    class Attributes(Element.BlockLevel.Attributes):
        For = "for"
        Form = "form"
    pass

class Legend(Element.BlockLevel):
    """
    Represents a caption for the content of its parent <fieldset>.
    """
    pass

class Meter(Element.BlockLevel):
    """
    Represents either a scalar value within a known range or a fractional value.
    """
    class Attributes(Element.BlockLevel.Attributes):
        Form = "form"
        High = "high"
        Low = "low"
        Max = "max"
        Min = "min"
        Optimum = "optimum"
        Value = "value"
    pass

class OptGroup(Element.BlockLevel):
    """
    Creates a grouping of options within a <select> element.
    """
    class Attributes(Element.BlockLevel.Attributes):
        Disabled = "disabled"
        Label = "label"
    pass

class Option(Element.BlockLevel):
    """
    Used to define an item contained in a select, an <optgroup>, or a <datalist> element. As such, <option> can
    represent menu items in popups and other lists of items in an HTML document.
    """
    class Attributes(Element.BlockLevel.Attributes):
        Disabled = "disabled"
        Label = "label"
        Selected = "selected"
        Value = "value"
    pass

class Output(Element.BlockLevel):
    """
    Container element into which a site or app can inject the results of a calculation or the outcome of a user action.
    """
    class Attributes(Element.BlockLevel.Attributes):
        For = "for"
        Form = "form"
        Name = "name"
    pass

class Progress(Element.BlockLevel):
    """
    Displays an indicator showing the completion progress of a task, typically displayed as a progress bar.
    """
    class Attributes(Element.BlockLevel.Attributes):
        Form = "form"
        Max = "max"
        Value = "value"
    pass

class Select(Element.BlockLevel):
    """
    Represents a control that provides a menu of options.
    """
    class Attributes(Element.BlockLevel.Attributes):
        Autocomplete = "autocomplete"
        Disabled = "disabled"
        Form = "form"
        Multiple = "multiple"
        Name = "name"
        Required = "required"
        Size = "size"
    pass

class TextArea(Element.BlockLevel):
    """
    Represents a multi-line plain-text editing control, useful when you want to allow users to enter a sizeable
    amount of free-form text, for example, a comment on a review or feedback form.
    """
    class Attributes(Element.BlockLevel.Attributes):
        Autocomplete = "autocomplete"
        Cols = "cols"
        Dirname = "dirname"
        Disabled = "disabled"
        Enterkeyhint = "enterkeyhint"
        Form = "form"
        Inputmode = "inputmode"
        Maxlength = "maxlength"
        Minlength = "minlength"
        Name = "name"
        Placeholder = "placeholder"
        Readonly = "readonly"
        Required = "required"
        Rows = "rows"
        Wrap = "wrap"
    pass

class Details(Element.BlockLevel):
    """
    Creates a disclosure widget in which information is visible only when the widget is toggled into an "open" state.
    A summary or label must be provided using the <summary> element.
    """
    class Attributes(Element.BlockLevel.Attributes):
        Open = "open"
    pass

class Dialog(Element.BlockLevel):
    """
    Represents a dialog box or other interactive component, such as a dismissible alert, inspector, or subwindow.
    """
    class Attributes(Element.BlockLevel.Attributes):
        Open = "open"
    pass

class Summary(Element.BlockLevel):
    """
    Specifies a summary, caption, or legend for a details element's disclosure box. Clicking the <summary> element
    toggles the state of the parent <details> element open and closed.
    """
    pass

class Slot(Element.BlockLevel):
    """
    Part of the Web Components technology suite, this element is a placeholder inside a web component that you can
    fill with your own markup, which lets you create separate DOM trees and present them together.
    """
    pass

class Template(Element.BlockLevel):
    """
    A mechanism for holding HTML that is not to be rendered immediately when a page is loaded but may be instantiated
    subsequently during runtime using JavaScript.
    """
    pass

class Bgsound(Element.BlockLevel):
    """
    Sets up a sound file to play in the background while the page is used; use <audio> instead.
    """
    pass

class Content(Element.BlockLevel):
    """
    An obsolete part of the Web Components suite of technologies—was used inside of Shadow DOM as an insertion point,
    and wasn't meant to be used in ordinary HTML. It has now been replaced by the <slot> element, which creates a point
    in the DOM at which a shadow DOM can be inserted. Consider using <slot> instead.
    """
    pass

class Image(Element.Inline):
    """
    An ancient and poorly supported precursor to the <img> element. It should not be used.
    """
    pass

class Marquee(Element.BlockLevel):
    """
    Used to insert a scrolling area of text. You can control what happens when the text reaches the edges
    of its content area using its Attributess.
    """
    class Attributes(Element.BlockLevel.Attributes):
        Bgcolor = "bgcolor"
        Loop = "loop"
    pass

class Menuitem(Element.BlockLevel):
    """
    Represents a command that a user is able to invoke through a popup menu. This includes context menus, as well
    as menus that might be attached to a menu button.
    """
    pass