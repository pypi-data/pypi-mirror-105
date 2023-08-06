__version__ = '0.1.0'



FORMATASCIISTRING = '\x1b[?m'



class FormatString():
    def __init__(self, value=None):
        self.parts = []

        if (isinstance(value, str)):
            self.parts = [FormatStringPart(value)]

        elif (isinstance(value, FormatString)):
            self.parts = value.parts

        elif (isinstance(value, FormatStringPart)):
            self.parts = [value]

        elif (value != None):
            raise(TypeError(f'unsupported initialize type(s) for \'{type(self).__name__}\': \'{type(value).__name__}\''))


    def __repr__(self):
        res = ''
        for part in self.parts:
            res += part.__repr__()
        return(f'{res}')


    def asrawstring(self):
        res = ''
        for part in self.parts:
            res += part.asrawstring()
        return(f'{res}')


    def copy(self):
        res = FormatString()
        for part in self.parts:
            res.parts.append(part.copy())
        return(res)


    def __add__(self, other):
        new = self.copy()

        if (isinstance(other, str)):
            new.parts.append(FormatStringPart(other))

        elif (isinstance(other, FormatString)):
            new.parts += other.parts

        elif (isinstance(other, FormatStringPart)):
            new.parts.append(other.copy())

        else:
            raise(TypeError(f'unsupported operand type(s) for +: \'{type(self).__name__}\' and \'{type(other).__name__}\''))

        return(new)



class FormatStringPart():
    def __init__(self, value):
        self.part = ''
        self.colours = []

        if (isinstance(value, str)):
            self.part = value
            self.colours = []
        elif (isinstance(value, FormatStringPart)):
            self.part = value.part
            self.colours = value.colours
        else:
            raise(TypeError(f'unsupported initialize type(s) for \'{type(self).__name__}\': \'{type(value).__name__}\''))


    def __repr__(self):
        finalColours = ''
        for colour in self.colours:
            finalColours += FORMATASCIISTRING.replace("?", colour)
        return(f'{FORMATASCIISTRING.replace("?", "0")}{finalColours}{self.part}{FORMATASCIISTRING.replace("?", "0")}')


    def asrawstring(self):
        return(self.part)


    def copy(self):
        res = FormatStringPart(self.part)
        res.colours = self.colours.copy()
        return(res)



class ColouredString():
    def __init__(self):
        raise(TypeError(f'{type(self).__name__} can not be initialized'))


    def _addcolour(obj, colour: int):
        if (not isinstance(colour, str)):
            raise(TypeError(f'unsupported input type(s) for colourizer: \'{type(obj).__name__}\' for \'colour\''))

        if (isinstance(obj, str)):
            obj = FormatStringPart(obj)
            obj.colours = [colour]
            obj = FormatString(obj)
            return(obj)
        elif (isinstance(obj, FormatString)):
            obj = obj.copy()
            for part in obj.parts:
                part.colours.append(colour)
            return(obj)
        else:
            raise(TypeError(f'unsupported input type(s) for colourizer: \'{type(obj).__name__}\' for \'obj\''))


    class Reset():
        def all(value):
            '''
                Resets all formatting
            '''
            return(ColouredString._addcolour(value, '0'))
        def intensity(value):
            '''
                Resets bold and faint formatting
            '''
            return(ColouredString._addcolour(value, '22'))
        def italic(value):
            '''
                Resets italic formatting
            '''
            return(ColouredString._addcolour(value, '23'))
        def underlined(value):
            '''
                Resets underlined formatting
            '''
            return(ColouredString._addcolour(value, '24'))
        def blink(value):
            '''
                Resets blink and rapidblink formatting
            '''
            return(ColouredString._addcolour(value, '25'))
        def invert(value):
            '''
                Resets invert formatting
            '''
            return(ColouredString._addcolour(value, '27'))
        reverse = invert
        def conceal(value):
            '''
                Resets conceal formatting
            '''
            return(ColouredString._addcolour(value, '28'))
        hide = conceal
        def strikethrough(value):
            '''
                Resets strikethrough formatting
            '''
            return(ColouredString._addcolour(value, '29'))
        crossout = strikethrough
        def framed(value):
            '''
                Resets framed and encircled formatting
            '''
            return(ColouredString._addcolour(value, '54'))
        def overlined(value):
            '''
                Resets overlined formatting
            '''
            return(ColouredString._addcolour(value, '55'))
        def modscript(value):
            '''
                Resets superscript and subscript formatting

                Minty only
            '''
            return(ColouredString._addcolour(value, '75'))

        def colourFg(value):
            '''
                Resets the foreground colour
            '''
            return(ColouredString._addcolour(value, f'39'))

        def colourBg(value):
            '''
                Resets the foreground colour
            '''
            return(ColouredString._addcolour(value, f'49'))



    class Style():
        def bold(value):
            '''
                Increases font intensity
            '''
            return(ColouredString._addcolour(value, '1'))
        def faint(value):
            '''
                Decreases font intensity
            '''
            return(ColouredString._addcolour(value, '2'))
        def italic(value):
            '''
                Slants the font

                Not widely supported
                May be treated as:
                - invert (reverse)
                - blink
            '''
            return(ColouredString._addcolour(value, '3'))
        def underline(value):
            '''
                Places a line under the font
            '''
            return(ColouredString._addcolour(value, '4'))
        def blink(value):
            '''
                Slowly pulses the font between visible and not visible
            '''
            return(ColouredString._addcolour(value, '5'))
        def rapidblink(value):
            '''
                Quickly pulses the font between visible and not visible

                Not widely supported
            '''
            return(ColouredString._addcolour(value, '6'))
        def invert(value):
            '''
                Swaps the foreground and background colours

                Inconsistent emulation
            '''
            return(ColouredString._addcolour(value, '7'))
        reverse = invert
        def conceal(value):
            '''
                Hides the font

                Not widely supported
            '''
            return(ColouredString._addcolour(value, '8'))
        hide = conceal
        def strikethrough(value):
            '''
                Crosses out the font
            '''
            return(ColouredString._addcolour(value, '9'))
        crossout = strikethrough
        def doubleunderline(value):
            '''
                Places two lines under the font

                May be treated as:
                - reset intensity
            '''
            return(ColouredString._addcolour(value, '21'))
        def framed(value):
            '''
                Frames the font
            '''
            return(ColouredString._addcolour(value, '51'))
        def encircled(value):
            '''
                Encircles the font
            '''
            return(ColouredString._addcolour(value, '52'))
        def overlined(value):
            '''
                Places a line above the font
            '''
            return(ColouredString._addcolour(value, '53'))
        def superscript(value):
            '''
                Decreases the font size and aligns it at the top

                Minty only
            '''
            return(ColouredString._addcolour(value, '73'))
        def subscript(value):
            '''
                Decreases the font size and aligns it at the bottom

                Minty only
            '''
            return(ColouredString._addcolour(value, '74'))


    class ColourFg():
        def black(value):
            '''
                Changes the foreground colour
            '''
            return(ColouredString._addcolour(value, '30'))
        def red(value):
            '''
                Changes the foreground colour
            '''
            return(ColouredString._addcolour(value, '31'))
        def green(value):
            '''
                Changes the foreground colour
            '''
            return(ColouredString._addcolour(value, '32'))
        def yellow(value):
            '''
                Changes the foreground colour
            '''
            return(ColouredString._addcolour(value, '33'))
        def blue(value):
            '''
                Changes the foreground colour
            '''
            return(ColouredString._addcolour(value, '34'))
        def purple(value):
            '''
                Changes the foreground colour
            '''
            return(ColouredString._addcolour(value, '35'))
        def cyan(value):
            '''
                Changes the foreground colour
            '''
            return(ColouredString._addcolour(value, '36'))
        def white(value):
            '''
                Changes the foreground colour
            '''
            return(ColouredString._addcolour(value, '37'))
        def rgb(value, r, g, b):
            '''
                Changes the foreground colour
            '''
            if (not isinstance(r, int)):
                raise(TypeError(f'unsupported input type(s) for colourizer: \'{type(r).__name__}\' for \'r\''))
            elif (not isinstance(g, int)):
                raise(TypeError(f'unsupported input type(s) for colourizer: \'{type(g).__name__}\' for \'g\''))
            elif (not isinstance(b, int)):
                raise(TypeError(f'unsupported input type(s) for colourizer: \'{type(b).__name__}\' for \'b\''))
            elif (not (r >= 0 and r <= 255)):
                raise(TypeError(f'unsupported input values(s) for colourizer: \'{r}\' for \'r\''))
            elif (not (g >= 0 and g <= 255)):
                raise(TypeError(f'unsupported input values(s) for colourizer: \'{g}\' for \'g\''))
            elif (not (b >= 0 and b <= 255)):
                raise(TypeError(f'unsupported input values(s) for colourizer: \'{b}\' for \'b\''))
            return(ColouredString._addcolour(value, f'38;2;{r};{g};{b}'))
        def default(value):
            '''
                Resets the foreground colour
            '''
            return(ColouredString._addcolour(value, f'39'))


    class ColourBg():
        def black(value):
            '''
                Changes the background colour
            '''
            return(ColouredString._addcolour(value, '40'))
        def red(value):
            '''
                Changes the background colour
            '''
            return(ColouredString._addcolour(value, '41'))
        def green(value):
            '''
                Changes the background colour
            '''
            return(ColouredString._addcolour(value, '42'))
        def yellow(value):
            '''
                Changes the background colour
            '''
            return(ColouredString._addcolour(value, '43'))
        def blue(value):
            '''
                Changes the background colour
            '''
            return(ColouredString._addcolour(value, '44'))
        def purple(value):
            '''
                Changes the background colour
            '''
            return(ColouredString._addcolour(value, '45'))
        def cyan(value):
            '''
                Changes the background colour
            '''
            return(ColouredString._addcolour(value, '46'))
        def white(value):
            '''
                Changes the background colour
            '''
            return(ColouredString._addcolour(value, '47'))
        def rgb(value, r, g, b):
            '''
                Changes the background colour
            '''
            if (not isinstance(r, int)):
                raise(TypeError(f'unsupported input type(s) for colourizer: \'{type(r).__name__}\' for \'r\''))
            elif (not isinstance(g, int)):
                raise(TypeError(f'unsupported input type(s) for colourizer: \'{type(g).__name__}\' for \'g\''))
            elif (not isinstance(b, int)):
                raise(TypeError(f'unsupported input type(s) for colourizer: \'{type(b).__name__}\' for \'b\''))
            elif (not (r >= 0 and r <= 255)):
                raise(TypeError(f'unsupported input values(s) for colourizer: \'{r}\' for \'r\''))
            elif (not (g >= 0 and g <= 255)):
                raise(TypeError(f'unsupported input values(s) for colourizer: \'{g}\' for \'g\''))
            elif (not (b >= 0 and b <= 255)):
                raise(TypeError(f'unsupported input values(s) for colourizer: \'{b}\' for \'b\''))
            return(ColouredString._addcolour(value, f'48;2;{r};{g};{b}'))
        def default(value):
            '''
                Resets the background colour
            '''
            return(ColouredString._addcolour(value, f'49'))



FmtStr = FormatString
Reset = ColouredString.Reset
Style = ColouredString.Style
ColourFg = ColouredString.ColourFg
ColourBg = ColouredString.ColourBg



if (__name__ == '__main__'):
    colours = [
        ColourFg.default,
        ColourFg.black,
        ColourFg.red,
        ColourFg.green,
        ColourFg.yellow,
        ColourFg.blue,
        ColourFg.purple,
        ColourFg.cyan,
        ColourFg.white,
        Style.conceal,
        ColourBg.default,
        ColourBg.black,
        ColourBg.red,
        ColourBg.green,
        ColourBg.yellow,
        ColourBg.blue,
        ColourBg.purple,
        ColourBg.cyan,
        ColourBg.white,
    ]
    styles = [
        Style.faint,
        Reset.all,
        Style.bold,
        Style.italic,
        Style.underline,
        Style.blink,
        Style.rapidblink,
        Style.invert,
        Style.conceal,
        Style.strikethrough,
        Style.doubleunderline,
        Style.framed,
        Style.encircled,
        Style.overlined,
        Style.superscript,
        Style.subscript
    ]
    final = FmtStr()
    for colour in colours:
        line = FmtStr()
        for style in styles:
            line += style(colour.__name__[0].upper()) + ' '
        final += FormatString(' ') + colour(line) + '\n'
    print(final)
