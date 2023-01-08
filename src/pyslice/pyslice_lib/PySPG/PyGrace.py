from past.utils import old_div

#
# IMPLEMENTS A GRACE DATASET         ###########
#


class GraceDataSet:
    basdefault = {
        "hidden": "false",
        "type": "xy",
        "baseline type": 0,
        "comment": '"Cols 1:2"',
        "legend": '" "',
    }

    bassymbol = {
        " ": 1,
        "size": 0.65,
        "color": 1,
        "pattern": 1,
        "fill color": 1,
        "fill pattern": 0,
        "linewidth": 1.0,
        "linestyle": 1,
        "char": 65,
        "char font": 0,
        "skip": 0,
    }

    basline = {"type": 1, "linestyle": 1, "linewidth": 2.0, "color": 1, "pattern": 1}

    basfill = {"type": 0, "rule": 0, "color": 1, "pattern": 1}

    def __init__(self, n=0, d=[], gT="xy"):
        self.data = d
        self.name = n

        # copia todos los diccionarios
        self.default = self.basdefault.copy()
        self.symbol = self.bassymbol.copy()
        self.line = self.basline.copy()
        self.fill = self.basfill.copy()
        self.default["type"] = gT

    def __str__(self):
        return (
            "\n".join(
                [
                    "@    s" + str(self.name) + " " + a + " " + str(b)
                    for a, b in list(self.default.items())
                ]
            )
            + "\n"
            + "\n".join(
                [
                    "@    s" + str(self.name) + " symbol " + a + " " + str(b)
                    for a, b in list(self.symbol.items())
                ]
            )
            + "\n"
            + "\n".join(
                [
                    "@    s" + str(self.name) + " line " + a + " " + str(b)
                    for a, b in list(self.line.items())
                ]
            )
            + "\n"
            + "\n".join(
                [
                    "@    s" + str(self.name) + " fill " + a + " " + str(b)
                    for a, b in list(self.fill.items())
                ]
            )
        )


#
# IMPLEMENTS A GRACE GRAPH           #########
#
class GraceGraph:
    bdefault = {
        " ": "on",
        "hidden": "false",
        "type": "XY",
        "stacked": "false",
        "bar hgap": "0.000000",
    }

    bworld = {"xmin": 0.0, "xmax": 1.0, "ymin": 0.0, "ymax": 1.0}

    bview = {"xmin": 0.18, "xmax": 1.21, "ymin": 0.13, "ymax": 0.88}

    btitle = {" ": '" "', "font": 0, "size": 1.5, "color": 1}

    bsubtitle = {" ": '" "', "font": 0, "size": 1.0, "color": 1}

    baxes = {"scale": "Normal", "invert": "off"}

    baxis = {
        " ": "on",
        "type zero": "false",
        "offset": "0.0 , 0.0",
        "bar": "on",
        "bar color": 1,
        "bar linestyle": 1,
        "bar linewidth": 1.0,
        "label": '"x"',
        "label layout": "para",
        "label place": "auto",
        "label char size": 1.9,
        "label font": 1,
        "label color": 1,
        "label place": "normal",
        "tick": "on",
        "tick major": 0.5,
        "tick minor ticks": 1,
        "tick default": 6,
        "tick place rounded": "true",
        "tick": "in",
        "tick major size": 1.0,
        "tick major color": 1,
        "tick major linewidth": 1.0,
        "tick major linestyle": 1,
        "tick major grid": "off",
        "tick minor color": 1,
        "tick minor linewidth": 1.0,
        "tick minor linestyle": 1,
        "tick minor grid": "off",
        "tick minor size": 0.5,
        "ticklabel": "on",
        "ticklabel format": "general",
        "ticklabel prec": 5,
        "ticklabel formula": '""',
        "ticklabel append": '""',
        "ticklabel prepend": '""',
        "ticklabel angle": 0,
        "ticklabel skip": 0,
        "ticklabel stagger": 0,
        "ticklabel place": "normal",
        "ticklabel offset": "auto",
        "ticklabel offset": "0.00 , 0.01",
        "ticklabel start type": "auto",
        "ticklabel start": 0.0,
        "ticklabel stop type": "auto",
        "ticklabel stop": 0.0,
        "ticklabel char size": 1.36,
        "ticklabel font": 0,
        "ticklabel color": 1,
        "tick place": "both",
        "tick spec type": "none",
    }

    blegend = {
        "": "on",
        "loctype": "view",
        " ": "0.85, 0.8",
        "box color": 1,
        "box pattern": 1,
        "box linewidth": 1.0,
        "box linestyle": 1,
        "box fill color": 0,
        "box fill pattern": 1,
        "font": 0,
        "char size": 1.0,
        "color": 1,
        "length": 4,
        "vgap": 1,
        "hgap": 1,
        "invert": "false",
    }

    bframe = {
        "type": 0,
        "linestyle": 1,
        "linewidth": 1.0,
        "color": 1,
        "pattern": 1,
        "background color": 0,
        "background pattern": 0,
    }

    def __init__(self, n=0):
        self.default = self.bdefault.copy()
        self.world = self.bworld.copy()
        self.view = self.bview.copy()
        self.title = self.btitle.copy()
        self.subtitle = self.bsubtitle.copy()
        self.xaxes = self.baxes.copy()
        self.yaxes = self.baxes.copy()

        self.xaxis = self.baxis.copy()
        self.yaxis = self.baxis.copy()
        self.legend = self.blegend.copy()
        self.frame = self.bframe.copy()

        self.name = n

    def __str__(self):
        return (
            "\n".join(
                [
                    "@g" + str(self.name) + " " + a + " " + str(b)
                    for a, b in list(self.default.items())
                ]
            )
            + "\n@with g"
            + str(self.name)
            + "\n"
            + "\n".join(
                ["@    world " + a + " " + str(b) for a, b in list(self.world.items())]
            )
            + "\n"
            + "\n".join(
                ["@    view " + a + " " + str(b) for a, b in list(self.view.items())]
            )
            + "\n"
            + "\n".join(
                ["@    title " + a + " " + str(b) for a, b in list(self.title.items())]
            )
            + "\n"
            + "\n".join(
                [
                    "@    subtitle " + a + " " + str(b)
                    for a, b in list(self.subtitle.items())
                ]
            )
            + "\n"
            + "\n".join(
                ["@    xaxes " + a + " " + str(b) for a, b in list(self.xaxes.items())]
            )
            + "\n"
            + "\n".join(
                ["@    yaxes " + a + " " + str(b) for a, b in list(self.yaxes.items())]
            )
            + "\n"
            + "\n".join(
                ["@    xaxis " + a + " " + str(b) for a, b in list(self.xaxis.items())]
            )
            + "\n"
            + "\n".join(
                ["@    yaxis " + a + " " + str(b) for a, b in list(self.yaxis.items())]
            )
            + "\n"
            + "\n".join(
                [
                    "@    legend " + a + " " + str(b)
                    for a, b in list(self.legend.items())
                ]
            )
            + "\n"
            + "\n".join(
                ["@    frame " + a + " " + str(b) for a, b in list(self.frame.items())]
            )
            + "\n"
        )


#
# IMPLEMENTS A GRACE DOC        ################
#
class GraceDocument:
    #
    #:::~ Constants
    basdefault = {"version": 50100}

    baspage = {"size": "792,612", "scroll": "5%", "inout": "5%"}

    basmap_font = {
        0: ('"Times-Roman"', '"Times-Roman"'),
        1: ('"Times-Italic"', '"Times-Italic"'),
        2: ('"Times-Bold"', '"Times-Bold"'),
        3: ('"Times-BoldItalic"', '"Times-BoldItalic"'),
        4: ('"Helvetica"', '"Helvetica"'),
        5: ('"Helvetica-Oblique"', '"Helvetica-Oblique"'),
        6: ('"Helvetica-Bold"', '"Helvetica-Bold"'),
        7: ('"Helvetica-BoldOblique"', '"Helvetica-BoldOblique"'),
        8: ('"Courier"', '"Courier"'),
        9: ('"Courier-Oblique"', '"Courier-Oblique"'),
        10: ('"Courier-Bold"', '"Courier-Bold"'),
        11: ('"Courier-BoldOblique"', '"Courier-BoldOblique"'),
        12: ('"Symbol"', '"Symbol"'),
        13: ('"ZapfDingbats"', '"ZapfDingbats"'),
    }

    basmap_color = {
        0: ((255, 255, 255), '"white"'),
        1: ((0, 0, 0), '"black"'),
        2: ((255, 0, 0), '"red"'),
        3: ((0, 255, 0), '"green"'),
        4: ((0, 0, 255), '"blue"'),
        5: ((255, 255, 0), '"yellow"'),
        6: ((188, 143, 143), '"brown"'),
        7: ((220, 220, 220), '"grey"'),
        8: ((148, 0, 211), '"violet"'),
        9: ((0, 255, 255), '"cyan"'),
        10: ((255, 0, 255), '"magenta"'),
        11: ((255, 165, 0), '"orange"'),
        12: ((114, 33, 188), '"indigo"'),
        13: ((103, 7, 72), '"maroon"'),
        14: ((64, 224, 208), '"turquoise"'),
        15: ((0, 139, 0), '"green4"'),
    }

    def __init__(self):
        # copies all the dicts
        self.datasets = {}
        self.graph = GraceGraph()

        self.default = self.basdefault.copy()
        self.page = self.baspage.copy()
        self.map_font = self.basmap_font.copy()
        self.map_color = self.basmap_color.copy()

    def __str__(self):
        return (
            "\n".join(["@" + a + " " + str(b) for a, b in list(self.default.items())])
            + "\n"
            + "\n".join(
                ["@page " + a + " " + str(b) for a, b in list(self.page.items())]
            )
            + "\n"
            + "\n".join(
                [
                    "@map font " + str(a) + " to " + b + ", " + c
                    for a, (b, c) in list(self.map_font.items())
                ]
            )
            + "\n"
            + "\n".join(
                [
                    "@map color "
                    + str(a)
                    + " to ("
                    + str(b)
                    + ","
                    + str(c)
                    + ","
                    + str(d)
                    + "), "
                    + str(e)
                    for a, ((b, c, d), e) in list(self.map_color.items())
                ]
            )
        )

    #
    #
    #
    #
    #
    #

    def set_data(self, ls, legend="", graphType="xy"):
        newds = GraceDataSet(len(self.datasets), ls, graphType)
        newds.symbol[" "] = len(self.datasets) + 1
        newds.line["color"] = len(self.datasets) + 1
        newds.symbol["color"] = len(self.datasets) + 1
        if legend == "":
            legend = f"y{str(len(self.datasets))}"
        legend = f'"{legend}"'
        newds.default["legend"] = legend
        self.datasets[len(self.datasets)] = newds

    def set_world(self, minx, maxx, miny, maxy, tickx=None, ticky=None):

        if minx == maxx:
            minx -= 0.5
            maxx += 0.5

        if miny == maxy:
            miny -= 0.5
            maxy += 0.5
        if not tickx:
            tickx = old_div((maxx - minx), 4.0)
        if not ticky:
            ticky = old_div((maxy - miny), 4.0)

        self.graph.world["xmin"] = minx
        self.graph.world["xmax"] = maxx
        self.graph.world["ymin"] = miny
        self.graph.world["ymax"] = maxy

        self.graph.xaxis["tick major"] = tickx
        self.graph.yaxis["tick major"] = ticky

    def getRoundedValues(self, scale, a2, a1):
        import math

        sign1 = sign2 = 1
        if a1 < 0:
            sign1 = -1
        if a2 < 0:
            sign2 = -1
        aa1 = abs(a1)
        aa2 = abs(a2)
        scale1 = math.floor(math.log10(max(1e-10, aa1)))
        scale2 = math.floor(math.log10(max(1e-10, aa2)))

        int1 = eval(f"{aa1:e}"[0]) + 1
        int2 = eval(f"{aa2:e}"[0]) - 1

        if scale == "Normal":
            propose1 = sign1 * int1 * 10**scale1
            propose2 = sign2 * int2 * 10**scale2
            skip = abs(old_div((int1 * 10**scale1 - int2 * 10**scale2), 4))
            return propose2, propose1, old_div(propose1, 4)
        else:
            propose1 = 10 ** (scale1 + 1)
            propose2 = 10 ** (scale2 - 1)

            return propose2, propose1, 10 ** int((scale1 - scale2) + 1)

    def autoscale(self, autoscaleaxis="xy"):
        minx = 1e10
        maxx = -1e10
        miny = 1e10
        maxy = -1e10

        for it in list(self.datasets.values()):
            colx = [a[0] for a in it.data]
            coly = [a[1] for a in it.data]
            if len(colx) > 0:
                minx = min(minx, min(colx))
                maxx = max(maxx, max(colx))
            if len(coly) > 0:
                miny = min(miny, min(coly))
                maxy = max(maxy, max(coly))

        minx, maxx, tickx = self.getRoundedValues(self.graph.xaxes["scale"], minx, maxx)
        miny, maxy, ticky = self.getRoundedValues(self.graph.yaxes["scale"], miny, maxy)
        if autoscaleaxis.find("x") >= 0:
            self.graph.world["xmin"] = minx
            self.graph.world["xmax"] = maxx
            self.graph.xaxis["tick major"] = tickx

        if autoscaleaxis.find("y") >= 0:
            self.graph.world["ymin"] = miny
            self.graph.world["ymax"] = maxy

            self.graph.yaxis["tick major"] = ticky

    def set_labels(self, stx, sty):
        self.graph.xaxis["label"] = f'"{stx}"'
        self.graph.yaxis["label"] = f'"{sty}"'

    def set_title(self, st):
        self.graph.subtitle[" "] = f'"{st}"'

    def dump(self, outStream=None):
        import sys

        old_stdout = sys.stdout
        if outStream:
            sys.stdout = outStream

        print(self)
        print(self.graph)
        for i in list(self.datasets.keys()):
            print(self.datasets[i])
        for i in list(self.datasets.keys()):
            print(f"@target G{str(self.graph.name)}.S{str(i)}")
            print(f"@type {str(self.datasets[i].default['type'])}")
            print("\n".join(["\t".join(map(str, a)) for a in self.datasets[i].data]))
            print("\n&")

        sys.stdout = old_stdout

    def set_scale(self, x="Normal", y="Normal"):
        self.graph.xaxes["scale"] = x
        self.graph.yaxes["scale"] = y


#  Example of use
#
#  g1=GraceDocument()
#
#  g1.set_data([[0.12,0.001],[0.1,0.5],[0.2,0.6],[0.3,0.8]],"foo")
#  g1.set_data([[.1,.1],[0.1,0.4],[0.2,0.5],[0.3,0.9]])

#  g1.autoscale()
#  g1.set_labels("x","y")
#  g1.set_scale(x="Logarithmic",y="Logarithmic")
# g1.set_world(-1,1,-1,1)
#  g1.set_title("Foo")
#  g1.dump()
