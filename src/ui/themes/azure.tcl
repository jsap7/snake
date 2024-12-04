package require Tk 8.6

namespace eval ttk::theme::azure {
    variable colors
    array set colors {
        -fg             "#ffffff"
        -bg             "#1e1e1e"
        -disabledfg     "#666666"
        -selectfg       "#ffffff"
        -selectbg       "#007acc"
        -accent         "#4CAF50"
        -accenthover    "#66BB6A"
        -accentpress    "#43A047"
    }

    proc LoadImages {imgdir} {
        variable I
        foreach file [glob -directory $imgdir *.png] {
            set img [file tail [file rootname $file]]
            set I($img) [image create photo -file $file -format png]
        }
    }

    ttk::style theme create azure -parent default -settings {
        ttk::style configure . \
            -background $colors(-bg) \
            -foreground $colors(-fg) \
            -troughcolor $colors(-bg) \
            -focuscolor $colors(-selectbg) \
            -selectbackground $colors(-selectbg) \
            -selectforeground $colors(-selectfg) \
            -insertwidth 1 \
            -insertcolor $colors(-fg) \
            -fieldbackground $colors(-bg) \
            -font {"Helvetica" 12} \
            -borderwidth 1 \
            -relief flat

        ttk::style configure TButton \
            -padding {8 4 8 4} \
            -anchor center \
            -foreground $colors(-fg)

        ttk::style configure Accent.TButton \
            -padding {15 10} \
            -anchor center \
            -foreground $colors(-fg) \
            -background $colors(-accent) \
            -font {"Helvetica" 14 bold}

        ttk::style map TButton \
            -background [list disabled $colors(-bg) \
                active $colors(-selectbg) \
                pressed $colors(-selectbg) \
                hover $colors(-selectbg)] \
            -foreground [list disabled $colors(-disabledfg)]

        ttk::style map Accent.TButton \
            -background [list disabled $colors(-bg) \
                active $colors(-accentpress) \
                pressed $colors(-accentpress) \
                hover $colors(-accenthover)] \
            -foreground [list disabled $colors(-disabledfg)]

        ttk::style configure TFrame \
            -background $colors(-bg)

        ttk::style configure TLabel \
            -background $colors(-bg) \
            -foreground $colors(-fg)

        ttk::style configure TLabelframe \
            -background $colors(-bg) \
            -foreground $colors(-fg) \
            -borderwidth 2 \
            -relief groove

        ttk::style configure TLabelframe.Label \
            -background $colors(-bg) \
            -foreground $colors(-fg)

        ttk::style configure TScale \
            -background $colors(-bg) \
            -foreground $colors(-fg) \
            -troughcolor "#333333"

        ttk::style map TScale \
            -background [list active $colors(-selectbg)] \
            -troughcolor [list pressed "#444444" active "#444444"]
    }
}

proc set_theme {mode} {
    if {$mode eq "dark"} {
        ttk::style theme use azure
    }
} 