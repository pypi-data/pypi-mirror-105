# Modules from the standard library
from PIL import Image, ImageTk
import tempfile
# import decimal
import tkinter as tk
import os

from abc import ABC

# Nico's modules
import library.core


# decimal.getcontext().prec = 2


def _v_grid(*args):
    """ Uses grid() method to place elements vertically into a grid. """
    for index, element in enumerate(args):
        element.grid(column=0, row=index)


def _h_grid(*args):
    """ Uses grid() method to place elements horizontally into a grid. """
    for index, element in enumerate(args):
        element.grid(column=index, row=0)


class LabelBox(tk.Frame):
    def __init__(self, parent, field: library.core._GuiTextObj, text: str, limit=-1):
        super().__init__(parent)
        self.grid(sticky=tk.E)

        self.label = tk.Label(self, text=text)
        self.entry_box = tk.Entry(self, textvariable=field.text_obj.tk_nugget)

        self.visibility = tk.Checkbutton(self, text='Visible?', variable=field.visibility_obj.tk_nugget)

        _h_grid(self.label, self.entry_box, self.visibility)


class LabelSpinBox(tk.Frame):
    def __init__(self,
                 parent,
                 text: str,
                 initial_val,
                 ):
        super().__init__(parent)

        self._data = library.core.GuiSpaceObject(initial_val)

        self.label = tk.Label(self, text=text)
        self.spinbox = tk.Spinbox(self, textvariable=self._data.tk_nugget, from_=0, to=12)

        _h_grid(self.label, self.spinbox)

    @property
    def tk_obj(self):
        return self._data.tk_nugget

    @property
    def space(self) -> int:
        return int(self._data)


# class FlagsDiagram(LabelFrameContainer):
#     def __init__(self, parent, *args, **kwargs):
#         super().__init__(parent, *args, **kwargs)
#
#         self.var = library.core.TkDoubleVar(1.0)
#
#         s = tk.Radiobutton(self, value=0.8, text='Small (80%)')
#         m = tk.Radiobutton(self, value=1.0, text='Default (100%)')
#         l = tk.Radiobutton(self, value=1.2, text='Large (120%)')
#
#         for radio_button in [s, m, l]:
#             radio_button['variable'] = self.var
#
#         _h_grid(s, m, l)


# class FlagsPrint(LabelFrameContainer):
#     def __init__(self, parent, *args, **kwargs):
#         super().__init__(parent, *args, **kwargs)
#
#         self.var_svg = tk.BooleanVar()
#         self.var_svg.set(tk.TRUE)
#
#         self.var_png = tk.BooleanVar()
#
#         self.svg = tk.Checkbutton(self, text="Save as SVG ⎇ + s",
#                                   # command=self._toggle,  # Only necessary if callback is useful
#                                   variable=self.var_svg)  # self.uf.tk_export_to_svg)
#         self.png = tk.Checkbutton(self, text="Save as PNG ⎇ + p",
#                                   # command=self._toggle,  # Only necessary if callback is useful
#                                   variable=self.var_png)  # self.uf.tk_export_to_png)
#         for check_button in [self.svg, self.png]:
#             check_button['underline'] = 8
#
#         self.var_transparency = tk.BooleanVar()
#         self.var_transparency.set(tk.FALSE)
#         self.transparency = tk.Checkbutton(self, text="Transparency ⎇ + t>",
#                                            # command=self._toggle,  # Only necessary if callback is useful
#                                            underline=0,
#                                            variable=self.var_transparency)
#
#         _h_grid(self.svg, self.png, self.transparency)
#
#         self.var_file_name = tk.StringVar()
#         self.var_file_name.set("Final_file_name")
#
#         self.file_name = LabelBox(self, "File name", self.var_file_name)


class Canvas:
    def __init__(self, parent):
        self._canvas = tk.Canvas(
            master=parent,
            borderwidth=0,
            highlightthickness=0,
            relief=tk.FLAT,
            bg='gray',
            cursor='dot',
            # relief=tk.RIDGE,
            # height=250,u
            # scrollregion=(-75, -75, 300, 300)
        )
        v_scroll_bar = tk.Scrollbar(master=parent, orient=tk.VERTICAL)
        h_scroll_bar = tk.Scrollbar(master=parent, orient=tk.HORIZONTAL)
        v_scroll_bar.grid(row=0, column=1, sticky=tk.NS)
        h_scroll_bar.grid(row=1, column=0, sticky=tk.EW)

        v_scroll_bar.config(command=self._canvas.yview)
        h_scroll_bar.config(command=self._canvas.xview)

        self._canvas.config(
            xscrollcommand=h_scroll_bar.set,
            yscrollcommand=v_scroll_bar.set,
        )
        # self._canvas.yview_scroll(500, tk.UNITS)

        ## Use when tkinter configures the size of the widget
        # self.surface.bind('<Configure>', self._on_configure)

    def _on_configure(self, event):
        """Do something when tkinter configures the size of the widget..."""
        print("Configuring!!!!")
        print(event, event.width)

    @property
    def width(self):
        return self.surface.winfo_reqwidth()

    @property
    def height(self):
        return self.surface.winfo_reqheight()

    @property
    def surface(self):
        return self._canvas

    def _scale_content(self, scale_factor: float):
        """Resize the elements on the canvas by a constant factor"""
        self.surface.scale(
            "all",  # Scale all elements
            0,
            0,
            scale_factor,
            scale_factor,
        )

    def resize_widget(self, height, width):
        """Set size of tkinter Canvas widget."""
        self.surface.config(width=width, height=height)

    def _zoom_by_factor(self, scaling_factor):
        """Base method for scaling and resizing widget"""
        self._scale_content(scale_factor=scaling_factor)

        # The diagram collection's height and width are two pixels smaller than the widget-- why?
        mystery_pixels = 2

        # Casting the values to integers avoids any unexpected uncertainty from floating point inaccuracy
        new_height = int((self.surface.winfo_reqheight() - mystery_pixels) * scaling_factor)
        new_width = int((self.surface.winfo_reqwidth() - mystery_pixels) * scaling_factor)

        print("new_height is:", new_height)

        self.resize_widget(height=new_height, width=new_width)

        self.surface.master.update()

        # print(canvas.surface.winfo_geometry())
        # print("winfo_reqwidth is:", canvas.surface.winfo_reqwidth())
        # print("Scaling factor was:", self.scaling_factor.get(), "canvas winfo before:", canvas.surface.winfo_width())
        # print("diagram collection width:", diagram_collection.width)

    def zoom_dynamic(self, scaling_factor: float):
        """Scale canvas content widget window together."""
        if scaling_factor > 1:
            scaling_factor = 1.1
            self._zoom_by_factor(scaling_factor)
        elif scaling_factor < 1:
            scaling_factor = 0.9
            self._zoom_by_factor(scaling_factor)


class PreviewBox(tk.LabelFrame):
    """ Container for the preview box """

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.image_data = library.core.MetaImage()
        self.diagram_collection = library.core.DataDiagramCollection()

        self.canvas = Canvas(parent=self)

        _v_grid(
            # self.the_image,
            self.canvas.surface
        )

    def update_preview(self) -> None:
        """Set the picture of the preview box."""

        # Create new visualization based on the desired implementation
        # Canvas
        self.canvas.surface.delete("all")

        data_interface_canvas = library.core.DataInterfaceCanvas(
            diagram_collection=self.diagram_collection,
            canvas=self.canvas,
        )
        data_interface_canvas.draw_all_diagrams()

    def get_collection(self):
        return self.diagram_collection


class CorrectionControls(tk.LabelFrame):
    """ Container for the buttons at the bottom of the diagram """

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent.frame_2, *args, **kwargs)

        self.reset_everything = library.core.TkMetaButton(
            root=self,
            text="Reset everything\n <ctrl> + <shift>\n+ <backspace>",
            command=parent.fiasco)
        self.reset_chord = library.core.TkMetaButton(
            root=self,
            text="Reset chord\n <alt> + r",
            command=parent.chord_reset)
        self.previous_remove = library.core.TkMetaButton(
            root=self,
            text="Remove\n <shift> + <backspace>",
            command=parent.pop_previous)
        self.previous_correct = library.core.TkMetaButton(
            root=self,
            text="Redo \n <alt> + <backspace>",
            command=parent.correct_previous)
        self.gen_takemitsu_chord = library.core.TkMetaButton(
            root=self,
            text="generate \nTakemitsu chord\n<alt> + t",
            command=lambda callback=parent.chord.generate_takemitsu_chord: parent._func_and_reload_sandbox(callback))
        self.add_to_list = library.core.TkMetaButton(
            root=self,
            text="Enter new diagram\n<return>",
            command=parent.add_diagram_to_list)

        for button in [self.reset_everything, self.previous_remove, self.previous_correct]:
            button.disable()

        for index, element in enumerate([self.reset_everything,
                                         self.reset_chord,
                                         self.previous_remove,
                                         self.previous_correct,
                                         self.add_to_list,
                                         self.gen_takemitsu_chord]):
            element.button.grid(column=index, row=0)


class AppControls(tk.LabelFrame):
    def __init__(self, parent, file_name_object, *args, **kwargs):
        super().__init__(parent.strip, *args, **kwargs)

        self.file_name = LabelBox(self, file_name_object, text="File name:")
        self.ask_name = library.core.TkMetaButton(self, text="Choose file",
                                                  command=parent.file_name_object.name_chooser)
        self.render = library.core.TkMetaButton(self, text="Render", command=parent.print)
        self.exit_app = library.core.TkMetaButton(self, text="Cancel <ESC>", command=parent.exit_app)

        _h_grid(
            self.file_name,
            self.ask_name.button,
            self.render.button,
            self.exit_app.button,
        )


class ChordInputBox(tk.LabelFrame):
    """ The container for chord input """

    def __init__(self,
                 parent,
                 tk_chord: library.core.TkDiagram,
                 size_mod: tk.DoubleVar,
                 *args, **kwargs
                 ):
        super().__init__(parent, *args, **kwargs)

        self.label = LabelBox(
            parent=self,
            field=tk_chord.label,
            text='Label'
        )
        self.preview_box = PreviewBox(
            parent=self,
            text="Input sandbox",
        )

        self._grid_everything()

    def _grid_everything(self):
        _v_grid(
            self.label,
            # self.one_liner,
            self.preview_box,
            # self.fingering,
            # self.neck_position,
        )


class SpacesBox(tk.LabelFrame):
    """ The container for String and Fret space widgets """

    def __init__(self, parent, interspersion, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # self.courses = LabelSpinBox(parent=self,
        #                             text="String space <shift> + <left/right>",
        #                             initial_val=6,
        #                             )
        # self.frets = LabelSpinBox(parent=self,
        #                           text="Position space <shift> + <up/down>",
        #                           initial_val=4
        #                           )

        self.sbd_box = tk.Entry(self, textvariable=interspersion)

        self.input_var = tk.StringVar()
        self.input_var.set('Chord')

        self.input_chord = tk.Radiobutton(self, text='Chord input', variable=self.input_var, value='Chord')
        self.input_scale = tk.Radiobutton(self, text='Scale input', variable=self.input_var, value='Scale')

        self._grid_everything()

    def _grid_everything(self):
        _v_grid(
            # self.courses,
            # self.frets,
            self.sbd_box
        )

    @property
    def tk_obj_frets(self):
        return self.input_chord.frets.tk_obj

    @property
    def fret_space(self):
        return self.frets.space


class MasterTk:
    def __init__(self, root):
        self.root = root

        self.scaling_factor: tk.DoubleVar = tk.DoubleVar(value=1.0)
        self.pixel_interspersion = tk.IntVar(value=0)

        """ future features:
                -automatically add x's to diagram
                -global title
                -develop 'teaching mode' with visual feedback
                
        """

        self.file_name_object = library.core.TkFileObject()

        self.chord = library.core.TkDiagram()

        self.frame_1 = tk.Frame(root)
        self.frame_2 = tk.Frame(root)
        self.strip = tk.Frame(root)

        self.chord_input_box = ChordInputBox(
            parent=self.frame_1,
            tk_chord=self.chord,
            text="Chord Input",
            size_mod=self.scaling_factor
        )

        self.spaces_box = SpacesBox(
            parent=self.frame_1,
            text="Strings and Frets",
            interspersion=self.pixel_interspersion
        )
        self.render_preview = PreviewBox(
            parent=self.frame_2,
            text="Render preview",

        )
        self.correction_controls = CorrectionControls(
            parent=self,
            text="Correction controls"
        )
        self.app_controls = AppControls(
            parent=self,
            file_name_object=self.file_name_object,
            text="App Controls",
        )

        self._grid_everything()

        # #################################################################
        self._initiate_key_bindings()
        # self._update_render_preview()
        self._update_sandbox()

    @staticmethod
    def exit_app(event) -> None:
        exit()

    def bind_mouse_wheel_roman_numeral(self, event) -> None:
        """ Method to change the position indication via scroll wheel. """

        # Scroll wheel up
        if event.num == 4:
            self.chord.position_marker.increment()
        # Scroll wheel down
        if event.num == 5:
            self.chord.position_marker.decrement()

        self._update_sandbox()

    def bind_mouse_wheel_zoom(self, event) -> None:
        """ Zooms the chord preview in and out."""

        # Todo: zooming the diagram misplaces the dots
        canvas = self.chord_input_box.preview_box.canvas
        diagram_collection = self.chord_input_box.preview_box.diagram_collection

        max_width = 400
        min_width = 100

        # # scroll wheel up
        if event.num == 4:
            if canvas.width < max_width:
                self.scaling_factor.set(self.scaling_factor.get() + 0.1)

        # # scroll wheel down
        if event.num == 5:
            if canvas.width > min_width:
                self.scaling_factor.set(self.scaling_factor.get() - 0.1)

        self._update_sandbox()

    def bind_mouse_wheel_fingering(self, event) -> None:
        """ Assigns fretting hand fingerings to dots on the sandbox preview. """
        grid_click = self.get_grid_click(event)
        node_already_there = self.chord.neo_nodes.check_for_node_at(grid_click.was_near_course, grid_click.was_near_fret)

        if node_already_there:
            selected_node = self.chord.neo_nodes.get_node_at(grid_click.was_near_course, grid_click.was_near_fret)
            if event.num == 4:  # scroll wheel up
                selected_node.fancy_fingering.increment()
            elif event.num == 5:  # scroll wheel down
                selected_node.fancy_fingering.decrement()

        self._update_sandbox()

    def get_grid_click(self, event):
        diagram_collection = self.chord_input_box.preview_box.diagram_collection
        diagram_collection.append(self.chord.unwrap(scaling_factor=self.scaling_factor.get()))
        interface_to_canvas = library.core.DataInterfaceCanvas(
            diagram_collection=diagram_collection,
            canvas=None,
        )
        grid_click = library.core.GridClick(event=event, interface=interface_to_canvas)
        return grid_click

    def bind_click_left_note_input(self, event) -> None:
        """ Creates a note node at the grid address closest to the user's click. """
        grid_click = self.get_grid_click(event=event)

        node_exists_at_address = self.chord.neo_nodes.check_for_node_at(
            grid_click.was_near_course,
            grid_click.was_near_fret
        )

        if grid_click.was_within_active_click_zone and not node_exists_at_address:
            self.chord.neo_nodes.delete_possible_x_on_course(grid_click.was_near_course)

            self.chord.make_new_node_at(
                desired_string=grid_click.was_near_course,
                desired_fret=grid_click.was_near_fret
            )
        elif grid_click.was_within_active_click_zone and node_exists_at_address and grid_click.was_near_fret == 0:
            self.chord.neo_nodes.node_morph_xo(grid_click.was_near_course)

        self._update_sandbox()

    def click_right_note_remove(self, event) -> None:
        """ Removes the note the user clicked on. """
        grid_click = self.get_grid_click(event=event)

        node_exists_at_address = self.chord.neo_nodes.check_for_node_at(
            course=grid_click.was_near_course,
            position=grid_click.was_near_fret
        )

        if grid_click.was_within_active_click_zone and node_exists_at_address:
            unwanted_index = self.chord.neo_nodes.get_nodes_index(grid_click.was_near_course, grid_click.was_near_fret)
            self.chord.neo_nodes.data.pop(unwanted_index)

        self._update_sandbox()

    def _grid_everything(self) -> None:
        this_list = [self.frame_1,
                     self.frame_2,
                     self.strip,
                     self.render_preview,
                     self.chord_input_box,
                     # self.scale_input_box,
                     self.spaces_box,
                     # self.flags_diagram,
                     # self.flags_print,
                     self.correction_controls,
                     self.app_controls]

        for index, element in enumerate(this_list):
            element.grid(column=0, row=index)

    def _activate_correction_controls(self) -> None:
        self.correction_controls.reset_everything.enable()
        self.correction_controls.previous_remove.enable()
        self.correction_controls.previous_correct.enable()

    def _update_sandbox(self, event=None) -> None:
        event if event else ...
        sandbox = self.chord_input_box.preview_box

        sandbox.diagram_collection.collection.clear()
        sandbox.canvas.surface.delete("all")

        diagram = self.chord.unwrap(scaling_factor=self.scaling_factor.get())
        sandbox.diagram_collection.pixel_interspersion = self.pixel_interspersion.get()

        sandbox.diagram_collection.append(diagram=diagram)
        sandbox.update_preview()

    def _update_render_preview(self) -> None:
        """Update the preview window of the final render."""
        if len(self.render_preview.diagram_collection.collection) > 0:
            self._activate_correction_controls()

        self.render_preview.update_preview()
        self.file_name_object.set_automatic_filename()

    def _initiate_key_bindings(self) -> None:
        """Binds key combinations with callbacks.

            Tkinter bindings always pass an event argument -- even if not explicitly passed.
            As a result, all callback functions must be defined with at least one parameter
            to receive the event object.

            Also: Functions referenced with parentheses get evaluated in place!
                Reference them without parentheses: 'callback' vs. 'callback()'

            Passing arguments
                Lambda expressions:
                    Event data is bound to the first defined parameter.
                    Define at least one parameter for event data. Doing otherwise will halt
                        execution and result in an error.
                    To pass zero arguments: Declare only the event variable.
                    To pass N arguments: Define N+1 parameters. Event data is assigned to the first.


            In the definition of the callback function:
                Tkinter always sends event data with callbacks from bindings. Regular function calls obviously do not.
                Function calls that don't send event data can be accommodated by defining the event parameter
                as an optional keyword argument: 'event=None'."""

        def test_callback(event):
            print(event)

        self.root.bind('<Control-k>', test_callback)

        combos = [
            # Increment/Decrement string fret spaces.
            ('<Shift-Right>', lambda evt, s=self.chord.course_space: self._func_and_reload_sandbox(s.increment)),
            ('<Shift-Down>', lambda evt, s=self.chord.position_space: self._func_and_reload_sandbox(s.increment)),
            ('<Shift-Left>', lambda evt, s=self.chord.course_space: self._func_and_reload_sandbox(s.decrement)),
            ('<Shift-Up>', lambda evt, s=self.chord.position_space: self._func_and_reload_sandbox(s.decrement)),

            # Add to list
            ('<Return>', self.add_diagram_to_list),

            # Render
            self.root.bind('<Control-Return>', self.print),

            # Remove / correct previous diagrams
            ('<Alt-r>', lambda event, callback=self.chord.reset: self._func_and_reload_sandbox(callback)),
            ('<Shift-BackSpace>', self.pop_previous),
            # lambda event, callback=self.render_preview.diagram_collection.meta_pop: self.func_update(callback)),
            ('<Alt-BackSpace>', self.correct_previous),

            # Reset everything
            ('<Control-Shift-BackSpace>', self.fiasco),

            # Generate random input
            ('<Alt-t>',
             lambda event, callback=self.chord.generate_takemitsu_chord: self._func_and_reload_sandbox(callback)),

            # # Toggle options
            # ('<Alt-s>', self.add_frame),
            # ('<Alt-s>', lambda event: self.flags_print.svg.toggle()),
            # ('<Alt-p>', lambda event: self.flags_print.png.toggle()),
            # ('<Alt-t>', lambda event: self.flags_print.transparency.toggle()),

            # Exit app
            ('<Escape>', self.exit_app),
        ]

        for thing in combos:
            self.root.bind(thing[0], thing[1])

        canvas = self.chord_input_box.preview_box.canvas.surface

        canvas.bind('<Button 1>', self.bind_click_left_note_input)
        canvas.bind('<Button 3>', self.click_right_note_remove)
        canvas.bind('<Control Button-4>', self.bind_mouse_wheel_fingering)
        canvas.bind('<Control Button-5>', self.bind_mouse_wheel_fingering)
        canvas.bind('<Control Shift Button-4>', self.bind_mouse_wheel_roman_numeral)
        canvas.bind('<Control Shift Button-5>', self.bind_mouse_wheel_roman_numeral)

        canvas.bind('<Button-4>', self.bind_mouse_wheel_zoom)
        canvas.bind('<Button-5>', self.bind_mouse_wheel_zoom)

    def chord_reset(self, event=None):
        """Reset chord data, then update sandbox preview"""
        event if event else ...
        self.chord.reset()
        self._update_sandbox()

    def _func_and_reload_sandbox(self, callback, event=None, *args) -> None:
        """Run callback function and update the sandbox preview."""
        event if event else ...
        callback(*args)
        self._update_sandbox()

    def add_diagram_to_list(self, event=None):
        """Load sandbox data into the render queue, then update the render preview."""
        event if event else ...
        self.render_preview.diagram_collection.append(self.chord.unwrap(self.scaling_factor.get()))
        self.render_preview.diagram_collection.pixel_interspersion = self.pixel_interspersion.get()
        self._update_render_preview()
        self.chord_reset()

    def print(self, event=None) -> None:
        """Initiate final render to file."""
        event if event else ...

        # raise NotImplementedError()
        file_path_and_name = str(self.file_name_object)

        if file_path_and_name == '':
            file_path_and_name = self.file_name_object.name_chooser()

        final_path = self.file_name_object.extension_inspect(file_path_and_name)

        data_interface = library.core.DataInterfaceCanvas(
            diagram_collection=self.render_preview.diagram_collection,
            canvas=self.render_preview.canvas.surface
        )
        self.render_preview.canvas.surface.postscript(
            file=final_path,
            colormode="color",
            height=self.render_preview.canvas.height,
            width=self.render_preview.diagram_collection.width,

        )

    def fiasco(self, event=None) -> None:
        """Reset user interface to initial values. Discards all chord data.

            While all chord data is discarded, some things are persistent:
            *Course and fret spaces
            *etc etc"""
        event if event else ...
        self.render_preview.diagram_collection.collection.clear()

        for button in [self.correction_controls.reset_everything,
                       self.correction_controls.previous_remove,
                       self.correction_controls.previous_correct,
                       ]:
            button.disable()

        self.chord_reset()
        self._update_render_preview()

    def correct_previous(self, event=None) -> None:
        """Load the previously entered chord into the user interface and sandbox."""
        event if event else ...

        if len(self.render_preview.diagram_collection) > 0:
            last_diagram = self.render_preview.diagram_collection.collection.pop()
        else:
            last_diagram = library.core.DataDiagram()
        if len(self.render_preview.diagram_collection) == 0:
            self.chord.reset()

        self.pixel_interspersion.set(0)

        self._update_render_preview()
        self._load_previous_chord(self.chord, last_diagram)
        self._update_sandbox()

    def pop_previous(self, event=None) -> None:
        """Removes the last chord entered into the render queue."""
        event if event else ...
        if len(self.render_preview.diagram_collection) > 0:
            self.render_preview.diagram_collection.collection.pop()
            self._update_render_preview()

    def _load_previous_chord(self, input_field, previous) -> None:
        """Take data from the last chord and load it into the user interface."""

        input_field.label.set_to(str(previous.label))
        input_field.position_marker.set_to(str(previous.position_marker))
        input_field.course_space.set_to(len(previous.courses))
        input_field.position_space.set_to(len(previous.positions))
        self.chord.neo_nodes.collection_replace(previous.node_data)
