""" This module contains the classes for the app """
# Standard library imports
import datetime
import tkinter as tk
import random
from tkinter.filedialog import asksaveasfilename
import tempfile
import PIL  # from PIL import Image, ImageTk
# import warnings
from collections import UserString

# Third party imports
from abc import ABC, abstractmethod


# import svgwrite
# import drawSvg


class TakemitsuInputGen(ABC):
    available_labels = ['Dream', 'Sea', 'Water', 'Garden', 'ok...', 'wtf', 'again', 'sigh...']
    available_roman_numerals = ['', 'I', 'V', 'II', 'IV', 'IX', 'III', 'VII', 'VIII']

    @classmethod
    def label(cls) -> str:
        return random.choice(cls.available_labels)

    @classmethod
    def roman_numeral(cls) -> str:
        return random.choice(cls.available_roman_numerals)

    @classmethod
    def one_liner(cls, string_space: int, position_space: int) -> str:
        """ Generates a one-line for use as input for a chord diagram.
                Bug alert: input does not yet support two digit note representations at position >=10. """
        output = ''
        while len(output) < string_space:
            output += cls._input_gen_keyboard_tap_position(position_space)
        return output

    @classmethod
    def fingering(cls, one_liner: str) -> str:
        fingering = ''
        for index in range(len(one_liner)):
            fingering += cls._input_gen_keyboard_tap_fingering(one_liner[index])
        return fingering

    @classmethod
    def alt_t(cls, **kwargs):
        return cls.random_scale(
            course_space=kwargs['course_space'],
            position_space=kwargs['position_space'],
            # geometry=kwargs['geometry']
        )

    @classmethod
    def random_dot(cls, position, course, geometry):
        node = NoteDot(
            users_position=position,
            users_fingering=random.randint(1, 4),
            int_course=course,
            geometry=geometry,
        )
        return node

    @classmethod
    def random_open(cls, course, geometry):
        node = NoteCircle(
            int_course=course,
            geometry=geometry,
        )
        return node

    @classmethod
    def random_scale(cls, course_space: int, position_space: int):
        """Create a random set of notes on the fret diagram."""

        collection = []
        geometry = _GeometryNoteNode()

        for course in range(course_space):
            for position in range(position_space):
                test = random.randint(1, 3)
                if test == 1:
                    if position == 0:
                        x_or_o = random.randint(0, 1)
                        if x_or_o == 0:
                            node = cls.random_open(course, geometry)
                        else:
                            node = NoteCross(int_course=course, geometry=geometry)
                    else:
                        node = cls.random_dot(position, course, geometry)
                    collection.append(node)
                else:
                    pass
        return collection

    ####################### Static methods ##################

    @staticmethod
    def _input_gen_keyboard_tap_position(position_space: int) -> str:
        integer = random.randint(-2, int(position_space) - 1)
        return str(integer) if integer >= 0 else 'x'

    @staticmethod
    def _input_gen_keyboard_tap_fingering(corresponding_position: str) -> str:
        try:
            corresponding_position = int(corresponding_position)
        except ValueError:
            corresponding_position = -1

        return str(random.randint(1, 4)) if corresponding_position > 0 else 'x'


class TkMetaButton:
    def __init__(self, root, **kwargs):
        self.button = tk.Button(root, **kwargs)

    def disable(self):
        self.button['state'] = tk.DISABLED

    def enable(self):
        self.button['state'] = tk.NORMAL


class TkMetaVar(ABC):
    def __init__(self,
                 tk_container: [tk.StringVar, tk.IntVar, tk.BooleanVar, tk.DoubleVar],
                 initial_value: any = None
                 ):
        self._tk_var = tk_container(value=initial_value)

    @property
    def tk_nugget(self):
        return self._tk_var

    @abstractmethod
    def set_to(self, value):
        pass


# class TkDoubleVar(TkMetaVar):
#     def __init__(self, initial_value: float):
#         super().__init__(tk.DoubleVar, initial_value=initial_value)


class MetaImage:
    def __init__(self):
        self.photo = None

    def receive_raster_image(self, raster_data):
        temp = tempfile.TemporaryFile()
        temp.write(raster_data.pngData)

        pil_image = PIL.Image.open(temp)

        self.photo = PIL.ImageTk.PhotoImage(pil_image)


class _SpaceObject(ABC):
    def __init__(self, value: int, maximum: int):
        self.value = value
        self.maximum = maximum
        self.minimum = 1

    def __int__(self):
        return self.value

    def increment(self) -> None:
        if self.minimum < self.value < self.maximum:
            self.value += 1

    def decrement(self) -> None:
        if self.maximum > self.value > self.minimum:
            self.value += -1

    def set_to(self, value) -> None:
        self.value = value


class _PositionSpace(_SpaceObject):
    def __init__(self,
                 value: int = 4
                 ):
        maximum = 20
        super().__init__(value=value, maximum=maximum)


class _CourseSpace(_SpaceObject):
    def __init__(self,
                 value: int = 6
                 ):
        maximum = 11
        super().__init__(value=value, maximum=maximum)


class _TkIntVarContainer(TkMetaVar):
    """ This is the new, decoupled object """

    def __init__(self, initial_value: int):
        super().__init__(tk.IntVar, initial_value=initial_value)

        self._upper_limit = 20
        self._lower_limit = 1

    def __int__(self):
        return self.tk_nugget.get()

    def __bool__(self):
        return bool(self.tk_nugget.get())

    def _limit_check(self, value: int) -> bool:
        return value in range(self._lower_limit, self._upper_limit)

    def set_to(self, value: int):
        if self._limit_check(value):
            self.tk_nugget.set(value)

    def increase(self):
        self.tk_nugget.set(int(self) + 1)

    def decrease(self):
        self.tk_nugget.set(int(self) - 1)

    @staticmethod
    def increment(thingy: tk.IntVar, increment: int):
        """ Use this to increment course and position spaces. """
        minimum = 2  # These are also set in the spinbox values...
        maximum = 12  # should it be taken care of?
        value = thingy.get() + increment
        if value < minimum:
            value = minimum
        elif value > maximum:
            value = maximum
        thingy.set(value)


class _TkStringVarContainer(TkMetaVar):
    def __init__(self, value: str = ''):
        super().__init__(tk.StringVar, initial_value=value)

    def __str__(self):
        return self.tk_nugget.get()

    def set_to(self, value: str):
        self.tk_nugget.set(value)

    def pad_to(self, this_many: int) -> None:
        """ Pads or truncates the tk.StringVar length to match the comparison integer. """
        if str(self) == '':
            return
        while len(str(self)) < this_many:
            self.set_to(str(self) + 'x')
        while len(str(self)) > this_many:
            self.set_to(str(self)[:-1])

    def append_something(self, something: str):
        self.tk_nugget.set(self.tk_nugget.get() + something)

    def overwrite_at_position_n(self, new_character: str, n: int):
        if len(new_character) != 1:
            raise ValueError("text argument must have length 1.")

        string_as_list = list(str(self))
        string_as_list[n] = new_character

        new_value = ''.join(string_as_list)

        self.set_to(new_value)

    def delete_at_position_n(self, n):
        modified_string = str(self)[:n] + str(self)[n + 1:]
        self.set_to(modified_string)


class _TkBooleanVarContainer(TkMetaVar):
    def __init__(self, value: bool = True):
        super().__init__(tk.BooleanVar, initial_value=value)

    def __bool__(self):
        return self.tk_nugget.get()

    def set_to(self, value: bool):
        self.tk_nugget.set(value)

    def bool_flip(self):
        self.tk_nugget.set(not bool(self))


class _GuiTextObj(ABC):
    _default_value = ''

    def __init__(self,
                 value: str = '',
                 visibility: bool = True,
                 limit: int = -1
                 ):
        self.text_obj = _TkStringVarContainer(value)
        self.visibility_obj = _TkBooleanVarContainer(visibility)

    def __str__(self):
        return str(self.text_obj)

    def __len__(self):
        return len(str(self))

    def length_check(self):
        pass

    def set_to(self, value: str):
        """ Accesses inner object's method to modify the text value the value. """
        self.text_obj.set_to(value)

    @property
    def is_visible(self) -> bool:
        """ Returns the boolean visibility of the text object"""
        return bool(self.visibility_obj)

    def padded_to(self, this_many: int) -> str:
        """ Calls inner object's pad() method. Returns a string. """
        self.text_obj.pad_to(this_many)
        return str(self)

    def reset(self):
        self.text_obj.set_to(_GuiTextObj._default_value)

    def unwrap(self, geometry):
        return NotImplementedError()


class GuiSpaceObject(_TkIntVarContainer):
    def __init__(self, init_value: int):
        super().__init__(initial_value=init_value)


class TkLabelObj(_GuiTextObj):
    def __init__(self,
                 label: str = '',
                 is_visible: bool = True
                 ):
        super().__init__(label, visibility=is_visible)

    # def unwrap(self, geometry):
    #     return CoreLabelObject(users_label=str(self),
    #                            geometry=geometry,
    #                            )


class TkFileObject(_GuiTextObj):
    def __init__(self):
        # stamp = datetime.datetime.today()
        super().__init__()
        # self.set_automatic_filename()

    @staticmethod
    def name_chooser():
        return asksaveasfilename()

    def set_automatic_filename(self):
        stamp = datetime.datetime.today()
        self.set_to(stamp.strftime("%b%d_at_%H-%M-%S"))

    def set_file_name(self):
        pass

    def get_file_name(self):
        pass

    @staticmethod
    def extension_inspect(filename) -> str:
        """Validate the file extension."""
        extension = ".ps" if filename[-3:] != '.ps' else ''
        filename = filename + extension
        return filename


class TkNeckPosObj(_GuiTextObj):
    roman_numerals = [
        '', "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X",
        "XI", "XII", "XIII", "XIV", "XV", "XVI", "XVII", "XVIII", "XIX", "XX"
    ]

    def __init__(self,
                 value: str = '',
                 visibility: bool = True,
                 is_roman_numeral: bool = True,
                 ):
        super().__init__(value, visibility)
        self.is_roman_numeral = is_roman_numeral

    def __int__(self):
        position = -1
        try:
            position = int(str(self))
        except ValueError:
            for index, value in enumerate(self.roman_numerals):
                if str(self) == value:
                    position = index
                else:
                    pass
        finally:
            return position

    # def unwrap(self, geometry):
    #     return CoreNeckPositionObj(
    #         user_wrote=str(self),
    #         position=int(self),
    #         is_visible=self.is_visible,
    #         is_roman_numeral=self.is_roman_numeral,
    #         geometry=geometry,
    #     )


class _TkInputObjectBaseClass(ABC):
    def __init__(self,
                 num_courses: int,
                 num_positions: int,
                 # label: TkLabelObj,
                 # neck_position: TkNeckPosObj
                 ):
        self.course_space = GuiSpaceObject(num_courses)
        self.fret_space = GuiSpaceObject(num_positions)

        self.label = TkLabelObj()
        self.neck_position = TkNeckPosObj()

        self.fancy_neck_position = IterableRomanNumeral()

        self.neo_nodes = TkCollectionOfNodes(data=None)

    @abstractmethod
    def unwrap(self):
        pass


class TkOneLiner(_GuiTextObj):
    def __init__(self):
        super().__init__()


class TkFingering(_GuiTextObj):
    def __init__(self):
        super().__init__()

        # self.users_fingering = _GuiTextObj(users_fingering)


class TkDiagram:
    def __init__(self,
                 courses: int = 6,
                 positions: int = 4,
                 label: str = '',
                 ):
        self.course_space = _CourseSpace(value=courses)
        self.position_space = _PositionSpace(value=positions)

        self.label = TkLabelObj(label=label)

        self.position_marker = IterableRomanNumeral()
        self.neo_nodes = TkCollectionOfNodes()

    def make_new_node_at(self, desired_string, desired_fret):
        berry_bush = _NoteNodeFactory(desired_string, desired_fret, users_fingering='')
        self.neo_nodes.data.append(berry_bush.get_berry())

    def reset(self, event=None):
        event if event else ...
        foo = [
            self.label,
            self.position_marker,
            self.neo_nodes,
        ]
        [thing.reset() for thing in foo]

    def generate_takemitsu_chord(self, event=None):
        event if event else ...

        self.label.set_to(TakemitsuInputGen.label())
        # self.position_marker.set_to(TakemitsuInputGen.roman_numeral())

        self.neo_nodes.collection_replace(TakemitsuInputGen.alt_t(
            course_space=int(self.course_space),
            position_space=int(self.position_space),
        ))

    def unwrap(self, scaling_factor: float):
        data_diagram = DataDiagram(
            course_space=int(self.course_space),
            position_space=int(self.position_space),
            label=str(self.label),
            node_data=self.neo_nodes.as_data_node_collection,
            neck_position=str(self.position_marker),
            scaling_factor=scaling_factor
        )
        return data_diagram


class Point:
    def __init__(self, x=0, y=0):
        self._x = x
        self._y = y

    def __str__(self):
        return f'{self.x}, {self.y}'

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    def assign_xy_from_container(self, value):
        self.x = value.x
        self.y = value.y

    def translate(self, delta_x: int = 0, delta_y: int = 0):
        self.x += delta_x
        self.y += delta_y


class _GeometryBaseClass(ABC):
    ratio = (1 + 5 ** 0.5) / 2  # Golden ratio -- but this could be any ratio or a random ratio between a range

    def __init__(self, scaling_factor: float = 1.0):
        self.scaling_factor = scaling_factor
        self.base_unit = 20 * self.scaling_factor

    @abstractmethod
    def height(self, **args):
        pass

    @abstractmethod
    def width(self, **args):
        pass


class _GeometryDiagramCollection(_GeometryBaseClass):
    def __init__(self, scaling_factor: float = 1.0):
        super().__init__(scaling_factor=scaling_factor)

        self.padding = {
            'left': 0,
            'right': 0,
            'top': 0,
            'bottom': 0
        }

    def width(self, width_diagrams) -> int:
        width = sum([
            self.padding['left'],
            width_diagrams,
            self.padding['right'],
        ])
        return width

    def height(self, label_height, diagram_height):
        height = sum([
            self.padding['top'],
            label_height,
            diagram_height,
            self.padding['bottom'],
        ])
        return height


class _GeometryDiagram(_GeometryBaseClass):
    def __init__(self, scaling_factor: float = 1.0):
        super().__init__(scaling_factor=scaling_factor)

        self.dot_radius = (self.base_unit / self.ratio) * 0.85

        self.interval_course = self.base_unit * 0.75
        self.interval_fret = (self.ratio * self.base_unit) * 0.75

        self.padding = {
            'left': self.base_unit * 2,
            'right': self.base_unit * 2,
            'top': self.base_unit / 2,
            'bottom': self.base_unit / 2
        }

    def height(self, label_height, pixels_at_nut, grid_height, fret_stroke):
        height = sum([
            self.padding['top'],
            label_height,
            pixels_at_nut,
            grid_height,
            fret_stroke,
            self.padding['bottom']
        ])
        return int(height)

    def width(self, width_position_marker, grid_width):
        width = sum([
            self.padding['left'],
            width_position_marker,
            grid_width,
            self.padding['right']
        ])
        return width

    def height_grid(self, number_of_frets: int) -> int:
        return int(number_of_frets * self.interval_fret)

    def width_grid(self, number_of_courses: int):
        width = sum([
            # self.dot_radius,
            int(number_of_courses * self.interval_course),
            # self.dot_radius,
        ])
        return width

    @property
    def height_pixels_at_nut(self) -> int:
        """Number of pixels to add above the grid."""
        value = self.dot_radius  # dot midpoint (still missing the "nudge")
        value += self.dot_radius * 2  # dot diameter
        return int(value)

    # ##/////////// Origins etc ////////////////

    def origin_courses_calc(self, courses, origin_grid, grid_width) -> list:
        collection = []
        for index, course_obj in enumerate(courses):
            origin_course = Point(origin_grid.x, origin_grid.y)
            num_of_courses = len(courses) - 1

            # x = origin_grid.x  # This is the mod from multiple diagrams
            try:
                origin_course.x += (grid_width / num_of_courses) * index
            except ZeroDivisionError:
                origin_course.x += (grid_width / 1) * index
                origin_course.x += grid_width / 2

            # origin_course.y = self.origin.y

            collection.append(origin_course)

        return collection

    def origin_frets_calc(self, frets, origin_grid, grid_height) -> list:
        collection = []
        for position, fret_obj in enumerate(frets):
            num_of_positions = len(frets)
            num_of_frets = num_of_positions - 1

            origin_fret = Point(origin_grid.x, origin_grid.y)

            try:
                origin_fret.y += ((grid_height / num_of_frets) * position)
            except ZeroDivisionError as err:
                print(err)
                origin_fret.y = ((grid_height / 1) * position) + grid_height

            collection.append(origin_fret)

        return collection

    def origin_grid_calc(self, origin_diagram, position_marker_width: int, label_height: int, pixels_nodes_at_nut: int):
        x = sum([
            origin_diagram.x,
            self.padding['left'],
            position_marker_width,
        ])
        y = sum([
            origin_diagram.y,
            self.padding['top'],
            label_height,
            pixels_nodes_at_nut
        ])

        coordinate = Point(int(x), int(y))
        return coordinate

    def origin_label_calc(self, width_grid, origin_grid, pixels_at_nut, height_label):
        x = (width_grid / 2) + origin_grid.x

        y = origin_grid.y
        y -= pixels_at_nut
        y -= height_label / 2

        return Point(int(x), int(y))

    def origin_position_marker(self, origin_grid, width_pm):
        origin_position_marker = Point(origin_grid.x, origin_grid.y)
        origin_position_marker.x -= self.dot_radius
        origin_position_marker.x -= width_pm

        origin_position_marker.y = origin_grid.y
        return origin_position_marker


class _GeometryPositionMarker(_GeometryBaseClass):
    def __init__(self,
                 dot_radius,
                 scaling_factor: float = 1.0,
                 ):
        super().__init__(scaling_factor=scaling_factor)

        self.dot_radius = dot_radius

        self.padding = {
            'left': 0,
            'right': self.base_unit,
            'top': 0,
            'bottom': 0
        }

    def height(self):
        raise NotImplementedError()

    def width(self, text: str):
        if len(text) == 0:
            return 0
        else:
            i_width = self.dot_radius * 1
            v_width = self.dot_radius * 2
            x_width = self.dot_radius * 2

            width = 0

            for letter in text:
                if letter == 'I':
                    width += i_width
                elif letter == 'V':
                    width += v_width
                elif letter == 'X':
                    width += x_width
                elif letter == ' ':
                    width += x_width
                else:
                    raise ValueError

            width += self.padding['right']

            return width


class _GeometryLabel(_GeometryBaseClass):
    def __init__(self,
                 font_size,
                 scaling_factor: float = 1.0,
                 ):
        super().__init__(scaling_factor=scaling_factor)
        self.font_size = font_size
        self.canvas_anchor = 'center'

    def height(self, text: str) -> int:
        return self.font_size * self.scaling_factor if text else 0

    def width(self):
        raise NotImplementedError()


class _GeometryFret(_GeometryBaseClass):
    def __init__(self,
                 fret_stroke: int = 5,
                 scaling_factor: float = 1.0,
                 ):
        super().__init__(scaling_factor=scaling_factor)

        self.stroke = 1 / (self.ratio ** 3) * self.base_unit

    def height(self):
        raise NotImplementedError()

    def width(self, grid_width):
        line_cap = 0

        width = sum([
            line_cap,
            grid_width,
            line_cap
        ])
        return width


class _GeometryCourse(_GeometryBaseClass):
    def __init__(self,
                 course_stroke: int = 5,
                 scaling_factor: float = 1.0,
                 ):
        super().__init__(scaling_factor=scaling_factor)

        self.course_stroke = course_stroke * self.scaling_factor

    # def stroke(self, course_number: int = 0):
    #     # mod = 0.1 * (self.base_unit /2)
    #     # return (1 / (self.ratio ** 5) * self.base_unit) + (0.4 * course_number)
    #     return self.base_unit / 3 * course_number * self.scaling_factor

    def stroke(self, course_interval, course_number: int = 0):
        # mod = 0.1 * (self.base_unit /2)
        # return (1 / (self.ratio ** 5) * self.base_unit) + (0.4 * course_number)
        return course_interval / 3

    def height(self):
        raise NotImplementedError()

    def width(self, grid_width):
        line_cap = 0

        width = sum([
            line_cap,
            grid_width,
            line_cap
        ])
        return width


class _GeometryNoteNode(_GeometryBaseClass):
    def __init__(self,
                 scaling_factor: float = 1.0,
                 ):
        super().__init__(scaling_factor=scaling_factor)

        self.dot_radius = (self.base_unit / self.ratio) * 0.85

        # nudge = self.base_unit * 0.05  # Distance north to dot marker
        nudge = 0
        # self.dot_midpoint_translation = self.dot_radius + nudge
        self.dot_midpoint_translation = 0

        self.circle_stroke = self.base_unit / 10
        self.cross_mod = self.dot_radius / 2.5

    def height(self):
        return self.dot_radius * 2

    def width(self):
        return self.dot_radius * 2


class _Vector(ABC):
    def __init__(self, geometry):
        self.origin = Point()
        self.geometry = geometry

    def plot(self, washi):
        washi.append(self.vector)

    @property
    def pixel_width(self):
        raise Exception(f"{self.__class__.__name__} should implement its own pixel_width property.")

    @property
    def pixel_height(self):
        raise Exception(f"{self.__class__.__name__} should implement its own pixel_height property.")

    @property
    @abstractmethod
    def vector(self):
        pass


#
# class Grid:
#     def __init__(self, num_of_courses, num_of_positions, geometry):
#         self.origin = Point()
#         self.geometry = geometry
#
#         self.new_courses = [NewCourseObj(geometry) for course in range(num_of_courses)]
#
#         self.courses = _LineObjCollection(of_type=CourseObj, number_of_elements=num_of_courses, counting_down=False)
#         self.frets = _LineObjCollection(of_type=FretObj, number_of_elements=num_of_positions, counting_down=False)
#
#         self.courses.finalize(line_length=self.height, number_of_elements=num_of_courses, geometry=geometry)
#         self.frets.finalize(line_length=self.width, number_of_elements=num_of_positions, geometry=geometry)
#
#     @property
#     def height(self) -> int:
#         height = len(self.frets) * self.geometry.interval_fret
#         return height
#
#     @property
#     def width(self) -> int:
#         return int(len(self.courses) * self.geometry.interval_course)
#
#     def set_origin(self,
#                    diagram_origin: Point,
#                    diagram_padding: dict,
#                    neck_position_width,
#                    label_height,
#                    pixels_nodes_at_nut
#                    ) -> None:
#         x = sum([
#             diagram_origin.x,
#             diagram_padding['left'],
#             neck_position_width,
#         ])
#         y = sum([
#             diagram_origin.y,
#             diagram_padding['top'],
#             label_height,
#             pixels_nodes_at_nut
#         ])
#
#         coordinate = Point(int(x), int(y))
#
#         self.origin.assign_xy_from_container(coordinate)
#
#         self._set_origin_courses()
#         self._set_origin_frets()
#
#     def _set_origin_courses(self) -> None:
#         collection = []
#         for index, course_obj in enumerate(self.courses):
#             num_of_courses = len(self.courses) - 1
#
#             x = self.origin.x  # This is the mod from multiple diagrams
#             try:
#                 x += (self.width / num_of_courses) * index
#             except ZeroDivisionError:
#                 x += (self.width / 1) * index
#                 x += self.frets[0].components[0] / 2
#
#             y = self.origin.y
#
#             collection.append(Point(int(x), int(y)))
#
#         self.courses.set_origin_of_each_line(collection)
#
#     def _set_origin_frets(self) -> None:
#         collection = []
#         for position, fret_obj in enumerate(self.frets):
#             num_of_positions = len(self.frets)
#             num_of_frets = num_of_positions - 1
#
#             x = self.origin.x
#             y = self.origin.y
#
#             try:
#                 y += ((self.height / num_of_frets) * position)
#             except ZeroDivisionError as err:
#                 print(err)
#                 y = ((self.height / 1) * position) + self.height
#
#             collection.append(Point(int(x), int(y)))
#
#         self.frets.set_origin_of_each_line(collection)
#
#         # backwards = []
#         # for position in range(len(collection), 0, -1):
#         #     backwards.append(collection[position - 1])
#         # return backwards
#
#     def get_grid_coordinate(self, course_number: int, fret_number: int) -> Point:
#         x = self.courses[course_number].origin.x
#         y = self.frets[fret_number].origin.y
#         y -= self.geometry.dot_midpoint_translation
#
#         return Point(x, y)
#

class _LineObjCollection:
    def __init__(self, of_type, number_of_elements, counting_down=False):
        self.line_type = of_type
        self.is_reversed = counting_down
        self._collection = [line for line in range(number_of_elements)]

    def __len__(self):
        return len(self._collection)

    def __getitem__(self, item):
        return self._collection[item]

    def __repr__(self):
        return str(self._collection)

    def gen_new_line(self, geometry, length, mod_multiplier=0):
        stick = self.line_type(geometry=geometry, length=length)
        self._collection.append(stick)

    def finalize(self, geometry, line_length, number_of_elements):
        """Give all lines in the collection a uniform length."""
        of_all_elements = len(self)
        self._collection.clear()
        for value in range(number_of_elements):
            self.gen_new_line(geometry=geometry, length=line_length, mod_multiplier=value)

    def set_origin_of_each_line(self, list_of_origins: list):
        for index, line in enumerate(self._collection):
            line.origin.assign_xy_from_container(list_of_origins[index])


class _LineObjBaseClass(ABC):
    """ The LineObject is the parent class of Courses and Frets. """

    def __init__(self, components, geometry):
        # super().__init__(geometry=geometry)
        self.components = components
        self.geometry = geometry

    def __repr__(self):
        return f'{self.__class__.__name__}(components={self.components}, stroke_width={self.thickness})'

    @property
    @abstractmethod
    def thickness(self):
        pass

    @property
    def length(self):
        return max(self.components)


class FretObj(_LineObjBaseClass):
    def __init__(self, geometry, length):
        components = (length, 0)

        super().__init__(geometry=geometry, components=components)

    @property
    def thickness(self):
        return 1 / (self.geometry.ratio ** 3) * self.geometry.unit

    # @property
    # def vector(self):
    #     return VectorFactory.make_a_horizontal_line(self.thickness, self.origin, self.components)


class NewCourseObj:
    def __init__(self, geometry):
        pass


class CourseObj(_LineObjBaseClass):
    def __init__(self, geometry, length, mod_multiplier=0):
        self.thick_mod = 1.66 - 0.4 * mod_multiplier
        components = (0, length)

        super().__init__(components=components, geometry=geometry)

    @property
    def thickness(self):
        return (1 / (self.geometry.ratio ** 5) * self.geometry.unit) + self.thick_mod


# class _CoreTextObj(_Vector, ABC):
#     _font_family = "Century schoolbook"  # For SVG
#     _font = "Century schoolbook"  # For tk.Canvas
#     _center = True
#     _vertical_alignment = "bottom"  # possible values are 'top', 'middle', and 'bottom'
#     _canvas_anchor = 'center'  # Other values are 'n, s, e, w, ne, se, etc'
#
#     def __init__(self,
#                  geometry: _Geometry,
#                  text: str = '',
#                  font_size: int = 20,
#                  color: str = "black",
#                  transform: str = '',
#                  ):
#         super().__init__(geometry=geometry)
#
#         self._text = text
#         self._font_size = font_size
#         self._color = color
#         self._transform = transform
#
#     def __len__(self):
#         return len(self._text)
#
#     def __str__(self):
#         return self._text
#
#     def __bool__(self):
#         # bool('') returns False. Any other string value would return True.
#         return bool(self._text)
#
#     def __repr__(self):
#         return f'{self.__class__.__name__}(label={str(self)}, font_size={self._font_size})'
#
#     def exceptional_text_set(self, value: str):
#         self._text = value
#
#     @property
#     def vector(self) -> drawSvg.Text:
#         return VectorFactory.make_a_text_object(text=str(self),
#                                                 font_size=self._font_size,
#                                                 x=self.origin.x,
#                                                 y=self.origin.y,
#                                                 center=self._center,
#                                                 valign=self._vertical_alignment,
#                                                 font_family=self._font_family,
#                                                 fill=self._color,
#                                                 transform=self._transform)
#
#     @abstractmethod
#     def set_origin(self, **kwargs) -> None:
#         pass
#
#     def draw_on_canvas(self, canvas) -> None:
#         """Draw text onto the tkinter canvas."""
#         canvas.create_text(self.origin.x, self.origin.y,
#                            font=(self._font, int(self.font_size)),
#                            anchor=self._canvas_anchor,
#                            text=str(self)
#                            )
#

#
#     def __init__(self,
#                  geometry: _Geometry,
#                  users_label='',
#                  size_mod=1,
#                  ):
#         super().__init__(
#             text=users_label,
#             geometry=geometry,
#         )
#         self._text = users_label
#         # self._font_size = 25 * size_mod
#
#     @property
#     def font_size(self) -> int:
#         return int(25 * self.geometry.scaling_factor)
#
#     @property
#     def pixel_height(self) -> int:
#         return self.font_size if bool(self) else 0
#
#     def set_origin(self,
#                    origin_grid: Point,
#                    pixel_width_grid,
#                    pixels_at_nut,
#                    ) -> None:
#         x = (pixel_width_grid / 2) + origin_grid.x
#
#         y = origin_grid.y
#         y -= pixels_at_nut
#
#         coordinates = Point(int(x), int(y))
#
#         self.origin.assign_xy_from_container(coordinates)


# class VectorFactory:
#
#     @staticmethod
#     def make_a_horizontal_line(thickness, origin: Point, components):
#         line = drawSvg.Line(origin.x, origin.y, origin.x + components[0], origin.y,
#                             stroke_width=thickness,
#                             stroke='black',
#                             stroke_linecap='round'
#                             )
#         return line
#
#     @staticmethod
#     def make_a_vertical_line(thickness, origin: Point, components):
#         # # negative value plots the line from top to bottom (Necessary to agree with SVG origin)
#         line = drawSvg.Line(origin.x, origin.y, origin.x, origin.y + components[1],
#                             stroke_width=thickness,
#                             stroke='black',
#                             stroke_linecap='round'
#                             )
#         return line
#
#     @staticmethod
#     def make_a_text_object(text: str, font_size: int, x: float, y: float, center: bool, valign: str,
#                            font_family: str, fill: str, transform: str) -> drawSvg.Text:
#         vector = drawSvg.Text(text=text,
#                               fontSize=font_size,
#                               x=x,
#                               y=y,
#                               center=center,
#                               valign=valign,
#                               font_family=font_family,
#                               fill=fill,
#                               transform=transform
#                               )
#         return vector
#
#     @staticmethod
#     def make_background(x: float, y: float, width, height, fill: str):
#         rectangle = drawSvg.Rectangle(x=x,
#                                       y=y,
#                                       width=width,
#                                       height=height,
#                                       fill=fill
#                                       )
#         return rectangle
#
#     @staticmethod
#     def make_an_x_shape(x: float, y: float, node: list,
#                         stroke_width: int, stroke: str, fill: str, fill_opacity):
#         path = drawSvg.Path(stroke_width=stroke_width, stroke=stroke, fill=fill, fill_opacity=fill_opacity)
#         path.M(x, y)
#         path.c(-node[0], -node[0], node[1], -node[2], node[1], -node[3])
#         path.c(node[7], -node[4], -node[5], -node[6], -node[1], -node[3])
#         path.c(node[0], -node[0], node[2], node[1], node[3], node[1])
#         path.c(node[4], node[7], node[6], -node[5], node[3], -node[1])
#         path.c(node[0], node[0], -node[1], node[2], -node[1], node[3])
#         path.c(node[7], node[4], node[5], node[6], node[1], node[3])
#         path.c(-node[0], node[0], -node[2], -node[1], -node[3], -node[1])
#         path.c(-node[4], node[7], -node[6], node[5], -node[3], node[1])
#         path.Z()
#         return path
#
#     @staticmethod
#     def make_a_dot(x, y, radius, fill: str, stroke: str, stroke_width: int = 0):
#         return drawSvg.Circle(x, y, radius,
#                               fill=fill, stroke=stroke)


class ModuloList(ABC):
    def __init__(self, bank: list):
        self._bank = bank
        self._counter = 0

    def __str__(self):
        return str(self.value)

    def __bool__(self):
        return bool(self.value)

    @property
    def value(self):
        return self._bank[self._counter]

    @property
    def _max_index(self) -> int:
        """Get list index of the last element in the bank."""
        return len(self._bank) - 1

    def increment(self) -> None:
        """Move counter at index i to index i+1"""
        if 0 <= self._counter < self._max_index:
            self._counter += 1
        elif self._counter == self._max_index:
            self._counter = 0

    def decrement(self) -> None:
        """Move counter at index i to index i-1"""
        if 0 < self._counter <= self._max_index:
            self._counter -= 1
        elif self._counter == 0:
            self._counter = self._max_index

    def reset(self) -> None:
        """Reset counter to initial value"""
        self._counter = 0

    def set_to(self, value: int) -> None:
        self._counter = value


class IterableFingering(ModuloList):
    def __init__(self, initial_value: int = 0):
        _bank = ['', '1', '2', '3', '4']
        super().__init__(_bank)

        if initial_value:
            self._counter = initial_value


class IterableRomanNumeral(ModuloList):
    def __init__(self):
        _bank = [
            '', "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X",
            "XI", "XII", "XIII", "XIV", "XV", "XVI", "XVII", "XVIII", "XIX", "XX"
        ]
        super().__init__(_bank)

    def set_to(self, value: str) -> None:
        if value in self._bank:
            for index, roman_numeral in enumerate(self._bank):
                if value == roman_numeral:
                    self._counter = index
        else:
            raise ValueError("Bad position marker value")


class _NoteNodeFactory:
    def __init__(self, int_course: int, users_position: int, users_fingering: str):
        self.course = int_course
        self.position = users_position
        self.fingering = users_fingering

    def get_berry(self):
        """Returns note node object by fretboard position.

            Remember that user is inputting text. """
        # if self.position == 'x':
        #     return self._uniform_berry_payload(NoteCross)

        if self.position == 0:
            return self._uniform_berry_payload(NoteCircle)

        elif int(self.position) > 0:
            return self._uniform_berry_payload(NoteDot)

        else:
            raise ValueError(f"No protocol for using '{self.position}' as input")

    def _uniform_berry_payload(self, flavor):
        """Return a note node object of type flavor.

            This method is intended to standardize creation of NoteNodes."""
        return flavor(
            geometry=_GeometryNoteNode(),
            users_position=self.position,
            users_fingering=self.fingering,
            int_course=self.course,
        )


class _NoteNodeBaseClass(ABC):
    """Base class for note types:

        Note: NoteNode origins refer to the center of the object."""

    def __init__(self,
                 users_position: int,
                 geometry: _GeometryNoteNode = None,
                 int_course: int = 0,
                 scaling_factor: float = 1.0
                 ):
        self.geometry = geometry if geometry else _GeometryNoteNode(scaling_factor=scaling_factor)

        self._course = int_course
        self._position = users_position

        self.color = 'Black'

    def __repr__(self):
        return f'{self.__class__.__name__}(course={str(self._course)}, position={str(self._position)})'

    @property
    def address(self) -> tuple:
        return self.course, self.position_on_grid

    @property
    def course(self) -> int:
        return int(self._course)

    @property
    def position_on_grid(self) -> int:
        value = int(self._position)
        return value if value > -1 else 0


class NoteCross(_NoteNodeBaseClass):
    """ Entering an x or a dash creates a cross on the diagram. Entering a space in the one liner does not. """
    stroke = 'black'
    fill_opacity = 0.5

    def __init__(self,
                 geometry: _GeometryNoteNode = _GeometryNoteNode(),
                 int_course: int = 0,
                 ):
        super().__init__(
            users_position=0,
            int_course=int_course,
            geometry=geometry,
        )


class _RoundNoteObj(_NoteNodeBaseClass):
    def __init__(self,
                 geometry: _GeometryNoteNode,
                 users_position: int,
                 users_fingering: str = '',
                 int_course: int = 0,
                 ):
        super().__init__(
            users_position,
            geometry,
            int_course
        )

        self.fill = 'black'  # Open notes override this
        self.stroke = 'black'


class NoteDot(_RoundNoteObj):
    def __init__(self,
                 geometry: _GeometryNoteNode(),
                 users_position,
                 users_fingering: int = 0,
                 int_course: int = 0,
                 ):
        super().__init__(
            geometry=geometry,
            users_position=users_position,
            int_course=int_course
        )

        self.fancy_fingering = IterableFingering(users_fingering)

    @property
    def has_fingering(self) -> bool:
        return bool(self.fancy_fingering)


class NoteCircle(_RoundNoteObj):
    def __init__(self,
                 geometry: _GeometryNoteNode = _GeometryNoteNode(),
                 users_position: int = 0,
                 int_course: int = 0,
                 users_fingering: str = ''
                 ):
        super().__init__(
            geometry,
            users_position=users_position,
            int_course=int_course,
        )
        self.fill = 'white'

    @property
    def radius(self):
        return self.radius * 0.85

    @property
    def stroke_width(self):
        return self.radius / 3.8


class _OriginMixin:
    def __init__(self):
        self._origin = Point()

    @property
    def origin(self):
        return self._origin


class TkCollectionOfNodes:
    """A collection of node data for use by Tkinter gui.

        Note that this should remain in the Tk* classes...
        """

    def __init__(self):
        self.data = []

    @property
    def as_data_node_collection(self):
        new = DataNodeCollection()
        for node in self.data:
            new.data.append(node)
        return new

    def collection_replace(self, node_list: list):
        self.data.clear()
        for node in node_list:
            self.data.append(node)

    def get_nodes_index(self, course: int, position: int):
        for index, node in enumerate(self.data):
            if node.course == course and node.position_on_grid == position:
                return index

    def delete_possible_x_on_course(self, course_number):
        if self.check_for_node_at(course_number, position=0):
            # check if it's an x
            node_index = self.get_nodes_index(course_number, position=0)
            node = self.as_data_node_collection[node_index]
            # delete it
            if node.__class__.__name__ == NoteCross.__name__:
                self.as_data_node_collection.data.pop(node_index)

    def check_for_node_at(self, course: int, position: int) -> bool:
        for node in self.data:
            if node.course == course and node.position_on_grid == position:
                return True
        else:
            return False

    def node_morph_xo(self, course_number: int):
        """ Changes changes note nodes between circles and crosses. """
        if self.check_for_node_at(course=course_number, position=0):
            node = self.get_node_at(course=course_number, position=0)
            node_index = self.get_nodes_index(course=course_number, position=0)

            if node.__class__.__name__ == NoteCross.__name__:
                new_node = NoteCircle(int_course=course_number)
            elif node.__class__.__name__ == NoteCircle.__name__:
                new_node = NoteCross(int_course=course_number)
            else:
                new_node = NoteCross(int_course=course_number)

            self.data.pop(node_index)
            self.data.append(new_node)

    def get_node_at(self, course, position):
        if self.check_for_node_at(course, position):
            for node in self.data:
                if node.course == course and node.position_on_grid == position:
                    return node
        else:
            return None

    def reset(self):
        self.data.clear()


class _DataGridLine:
    def __init__(self,
                 index: int,
                 color: str
                 ):
        self.index = index
        self.color = color


class DataCourse(_DataGridLine):
    def __init__(self,
                 index: int = 0,
                 color: str = 'black',
                 scaling_factor: float = 1.0,
                 ):
        super().__init__(index=index, color=color)
        self.geometry = _GeometryCourse(scaling_factor=scaling_factor)


class DataFret(_DataGridLine):
    def __init__(self,
                 index: int = 0,
                 color: str = 'black',
                 scaling_factor: float = 1.0,
                 ):
        super().__init__(index=index, color=color)
        self.geometry = _GeometryFret(scaling_factor=scaling_factor)

    def height(self):
        raise NotImplementedError()

    def width(self):
        raise NotImplementedError()


class DataBackground:
    def __init__(self, color: str = 'white'):
        self.color = color


class DataLabel(UserString):
    def __init__(self,
                 value: str = '',
                 font_size: int = 25,
                 scaling_factor: float = 1.0,
                 ):
        super().__init__(seq=value)

        self.geometry = _GeometryLabel(font_size=font_size, scaling_factor=scaling_factor)

        # self.font_size = font_size
        self.font = "Century schoolbook"

    @property
    def height(self) -> int:
        return self.geometry.height(str(self))

    def width(self):
        raise NotImplementedError()


class DataNeckPosition(UserString):
    def __init__(self,
                 dot_radius,
                 value: str = '',
                 font_size: int = 25,
                 ):
        super().__init__(seq=value)
        self.geometry = _GeometryPositionMarker(dot_radius=dot_radius)

        self.font = "Century schoolbook"
        self.font_size = font_size
        self.canvas_anchor = 'w'

    @property
    def width(self):
        return self.geometry.width(text=str(self))


class DataNodeCollection:
    def __init__(self, data: list = None):
        self.data = data if data else []

    def __getitem__(self, item):
        return self.data[item]

    def __len__(self):
        return len(self.data)


class DataDiagram(_OriginMixin):
    def __init__(self,
                 course_space: int = 6,
                 position_space: int = 4,
                 label: str = 'Nico',
                 node_data=None,
                 neck_position: str = '',
                 background_color: str = 'white',
                 scaling_factor: float = 1.0,
                 ):
        super().__init__()
        self.geometry = _GeometryDiagram(scaling_factor=scaling_factor)

        self.label = DataLabel(value=label, scaling_factor=scaling_factor)
        self.position_marker = DataNeckPosition(value=neck_position, dot_radius=self.geometry.dot_radius)

        self.background = DataBackground(color=background_color)

        self.node_data = node_data if node_data else DataNodeCollection()

        self.courses = [DataCourse(index=index) for index in range(course_space)]
        self.positions = [DataFret(index=index) for index in range(position_space)]

    @property
    def height(self):
        height = self.geometry.height(
            label_height=self.label.height,
            pixels_at_nut=self.geometry.height_pixels_at_nut,
            grid_height=self.geometry.height_grid(number_of_frets=len(self.positions)),
            fret_stroke=self.positions[0].geometry.stroke,
        )
        return height

    @property
    def width(self):
        width = self.geometry.width(
            width_position_marker=self.position_marker.width,
            grid_width=self.geometry.width_grid(number_of_courses=len(self.courses))
        )
        return width

    @property
    def origin_courses(self) -> list:
        return self.geometry.origin_courses_calc(
            courses=self.courses,
            origin_grid=self.origin_grid,
            grid_width=self.geometry.width_grid(number_of_courses=len(self.courses))
        )

    @property
    def origin_frets(self) -> list:
        return self.geometry.origin_frets_calc(
            frets=self.positions,
            origin_grid=self.origin_grid,
            grid_height=self.geometry.height_grid(number_of_frets=len(self.positions))
        )

    @property
    def origin_grid(self):
        return self.geometry.origin_grid_calc(
            origin_diagram=self.origin,
            position_marker_width=self.position_marker.width,
            label_height=self.label.height,
            pixels_nodes_at_nut=self.geometry.height_pixels_at_nut
        )

    @property
    def origin_label(self):
        return self.geometry.origin_label_calc(
            width_grid=self.width_grid,
            origin_grid=self.origin_grid,
            pixels_at_nut=self.geometry.height_pixels_at_nut,
            height_label=self.label.height
        )

    @property
    def origin_position_marker(self):
        return self.geometry.origin_position_marker(
            origin_grid=self.origin_grid,
            width_pm=self.position_marker.width
        )

    @property
    def height_grid(self):
        return self.geometry.height_grid(number_of_frets=len(self.positions))

    @property
    def width_grid(self):
        return self.geometry.width_grid(number_of_courses=len(self.courses))


class DataDiagramCollection(_OriginMixin):
    def __init__(self,
                 title: str = '',
                 background_color: str = 'white',
                 pixel_interspersion: int = 0,
                 scaling_factor: float = 1.0
                 ):

        _OriginMixin.__init__(self)
        self.geometry = _GeometryDiagramCollection(scaling_factor=scaling_factor)

        self.collection = []
        self.label = DataLabel(value=title)
        self.background = DataBackground(background_color)

        # # Geometric values

        self.pixel_interspersion = pixel_interspersion

    def __getitem__(self, item):
        return self.collection[item]

    def __len__(self):
        return len(self.collection)

    def set_uniform_scaling(self) -> None:
        [diagram.set_scaling(self.geometry.scaling_factor) for diagram in self.collection]

    def append(self, diagram: DataDiagram) -> None:
        if not isinstance(diagram, DataDiagram):
            raise ValueError("Only objects of type DataDiagram may be added to the collection")
        diagram.origin.assign_xy_from_container(self.next_diagram_origin)
        self.collection.append(diagram)

    @property
    def next_diagram_origin(self) -> Point:
        x_value = int(self.width - self.geometry.padding['right'])
        padding_top = int(self.geometry.padding['top'])
        coordinate_of_write_head = Point(x=x_value, y=padding_top)
        return coordinate_of_write_head

    @property
    def height(self) -> int:
        max_height = 0
        for diagram in self.collection:
            max_height = diagram.height if diagram.height > max_height else max_height

        height = self.geometry.height(label_height=self.label.height, diagram_height=max_height)
        return height

    @property
    def width(self) -> int:
        width_diagrams = 0
        for diagram in self.collection:
            width_diagrams += diagram.width
        if len(self.collection) > 1:
            width_diagrams += self.pixel_interspersion * (len(self.collection) - 1)
        width = self.geometry.width(width_diagrams=width_diagrams)
        return width


class DataInterfaceCanvas:
    """ An interface to convert diagram data into a tkinter Canvas visualization."""

    def __init__(self, diagram_collection: DataDiagramCollection, canvas):
        self.diagram_collection: DataDiagramCollection = diagram_collection
        self.canvas = canvas

    def draw_all_diagrams(self) -> None:
        for diagram in self.diagram_collection:
            diagram: DataDiagram = diagram
            self._draw_diagram(diagram)

        max_diagrams_in_window = 5
        desired_width = self.diagram_collection.width
        if len(self.diagram_collection.collection) <= max_diagrams_in_window:
            max_width = desired_width
        else:
            working_width = 0
            for index, diagram in enumerate(self.diagram_collection):
                if index < max_diagrams_in_window:
                    working_width += diagram.width
                else:
                    break
            max_width = working_width

        self.canvas.resize_widget(
            width=max_width,
            height=self.diagram_collection.height
        )
        self.canvas.surface.config(
            scrollregion=(0, 0, self.diagram_collection.width, self.diagram_collection.height)
        )

    ##############################

    def _draw_diagram(self, diagram: DataDiagram) -> None:
        """Draw all the diagram elements onto the canvas."""
        self._draw_background(
            background=diagram.background,
            origin=diagram.origin,
            width=diagram.width,
            height=diagram.height
        )

        self._draw_grid(diagram=diagram,
                        origin_courses=diagram.origin_courses,
                        origin_frets=diagram.origin_frets,
                        )

        self._draw_label(
            diagram=diagram,
            origin=diagram.origin_label
        )

        self._draw_position_marker(
            diagram=diagram,
        )

        self._draw_nodes(
            node_data=diagram.node_data,
            course_origins=diagram.origin_courses,
            fret_origins=diagram.origin_frets,
            geometry=diagram.geometry
        )

    def _draw_position_marker(self, diagram: DataDiagram):
        self.canvas.surface.create_text(
            diagram.origin_position_marker.x,
            diagram.origin_position_marker.y,
            font=(diagram.position_marker.font,
                  int(diagram.geometry.scaling_factor * diagram.position_marker.font_size)),
            anchor=diagram.position_marker.canvas_anchor,
            text=str(diagram.position_marker)
        )

    def _draw_label(self, diagram: DataDiagram, origin: Point):
        self.canvas.surface.create_text(
            origin.x, origin.y,
            font=(diagram.label.font, int(diagram.geometry.scaling_factor * diagram.label.geometry.font_size)),
            anchor=diagram.label.geometry.canvas_anchor,
            text=str(diagram.label)
        )

    def _draw_background(self, background: DataBackground, origin: Point, width, height):
        """Draw a rectangular background on the tkinter canvas."""
        self.canvas.surface.create_rectangle(
            origin.x,
            origin.y,
            origin.x + width,
            origin.y + height,
            fill=background.color,
            width=0,
            outline="white",
        )

    def _draw_grid(self, diagram: DataDiagram, origin_courses, origin_frets) -> None:

        for course in diagram.courses:
            origin = origin_courses[course.index]
            self._draw_course(
                line=course,
                origin=origin,
                length=diagram.height_grid,
                course_interval=diagram.geometry.interval_course,
            )
        for fret in diagram.positions:
            origin = origin_frets[fret.index]
            self._draw_fret(
                line=fret,
                origin=origin,
                length=diagram.width_grid,
            )

    def _draw_course(self, line: DataCourse, origin: Point, length: int, course_interval):
        self.canvas.surface.create_line(
            origin.x,
            origin.y,
            origin.x,
            origin.y + length,
            width=line.geometry.stroke(course_interval=course_interval, course_number=line.index),
            capstyle=tk.ROUND,
        )

    def _draw_fret(self, line: DataFret, origin: Point, length: int):
        self.canvas.surface.create_line(
            origin.x,
            origin.y,
            origin.x + length,
            origin.y,
            width=line.geometry.stroke,
            capstyle=tk.ROUND
        )

    def _draw_nodes(self, node_data: list, course_origins: list, fret_origins: list, geometry):
        uniform_geometry = _GeometryNoteNode(scaling_factor=geometry.scaling_factor)
        font_size = int(15 * uniform_geometry.scaling_factor)

        for node in node_data:
            node: _NoteNodeBaseClass = node
            x = course_origins[node.course].x
            y = fret_origins[node.position_on_grid].y
            # y -= node.geometry.dot_midpoint_translation
            y -= uniform_geometry.dot_radius

            origin = Point(x, y)
            if isinstance(node, NoteDot):
                self._draw_dot(center_point=origin, radius=uniform_geometry.dot_radius)
                if node.has_fingering:
                    text_origin = Point(origin.x, int(origin.y + uniform_geometry.dot_radius / 2.5))
                    self._draw_fingering(
                        origin=text_origin,
                        text=str(node.fancy_fingering),
                        font_size=font_size
                    )
            elif isinstance(node, NoteCircle):
                self._draw_circle(
                    origin=origin,
                    geometry=uniform_geometry)
            elif isinstance(node, NoteCross):
                self._draw_cross(
                    origin=origin,
                    geometry=uniform_geometry)

    def _draw_cross(self, origin, geometry):
        mod = geometry.cross_mod
        ms = [
            (-1, +0),  # inside point
            (-1, -.5),  # inside handle
            (-2.3, -1.7),  # outside handle
            (-2, -2),  # outside point
        ]

        segment_1 = [
            (ms[0][0] * mod, ms[0][1]),  # inside point
            (ms[1][0] * mod, ms[1][1] * mod),  # inside handle
            (ms[2][0] * mod, ms[2][1] * mod),  # outside handle
            (ms[3][0] * mod, ms[3][1] * mod),  # outside point
        ]
        segment_2 = [(+y, +x) for x, y in list(reversed(segment_1))]
        segment_3 = [(-x, +y) for x, y in list(reversed(segment_2))]
        segment_4 = [(-x, +y) for x, y in list(reversed(segment_1))]
        segment_5 = [(+x, -y) for x, y in list(reversed(segment_4))]
        segment_6 = [(+x, -y) for x, y in list(reversed(segment_3))]
        segment_7 = [(-x, +y) for x, y in list(reversed(segment_6))]
        segment_8 = [(+x, -y) for x, y in list(reversed(segment_1))]

        control_points = list()

        control_points.append(segment_1)
        control_points.append(segment_2)
        control_points.append(segment_3)
        control_points.append(segment_4)
        control_points.append(segment_5)
        control_points.append(segment_6)
        control_points.append(segment_7)
        control_points.append(segment_8)

        def calc_segments(list_of_segments):
            big_list = []
            for segment in list_of_segments:
                p = segment

                # loop through segments and divide them into smaller bezier-curve-like segments.
                # Note that these values get "smoothed" by the polygon shape later on.
                n = 100
                for i in range(100):
                    t = i / n
                    x_0, y_0 = p[0][0], p[0][1]
                    x_1, y_1 = p[1][0], p[1][1]
                    x_2, y_2 = p[2][0], p[2][1]
                    x_3, y_3 = p[3][0], p[3][1]

                    x = (x_0 * (1 - t) ** 3 + x_1 * 3 * t * (1 - t) ** 2 + x_2 * 3 * t ** 2 * (1 - t) + x_3 * t ** 3)
                    y = (y_0 * (1 - t) ** 3 + y_1 * 3 * t * (1 - t) ** 2 + y_2 * 3 * t ** 2 * (1 - t) + y_3 * t ** 3)

                    big_list.append((x + origin.x, y + origin.y))
            return big_list

        vertices = calc_segments(control_points)
        self.canvas.surface.create_polygon([(x, y) for x, y in vertices], smooth=1, splinesteps=1000)

    def _draw_fingering(self, origin, text, font_size):
        self.canvas.surface.create_text(
            origin.x, origin.y,
            font=('Courier', font_size),
            anchor=tk.CENTER,
            text=text,
            fill='white',
        )

    def _draw_dot(self, center_point, radius):
        x0 = center_point.x - radius
        y0 = center_point.y - radius
        x1 = center_point.x + radius
        y1 = center_point.y + radius

        self.canvas.surface.create_oval(
            x0, y0, x1, y1,
            fill="black",
        )

    def _draw_circle(self, origin, geometry):
        x0 = origin.x - geometry.dot_radius + 2
        y0 = origin.y - geometry.dot_radius + 2
        x1 = origin.x + geometry.dot_radius - 2
        y1 = origin.y + geometry.dot_radius - 2

        self.canvas.surface.create_oval(x0, y0, x1, y1,
                                        fill="white",
                                        width=geometry.circle_stroke,
                                        activefill='#eee',
                                        activewidth=geometry.circle_stroke * 1.3
                                        )


class GridClick:
    clicked_around_a_course = False
    clicked_around_a_fret = False
    desired_string = None
    desired_fret = None

    def __init__(self, event, interface: DataInterfaceCanvas):
        self.event = event
        self.interface = interface

    @property
    def clicked_in_node_zone(self):
        """Check if the event click was in a node zone"""
        return bool(self.clicked_around_a_course and self.clicked_around_a_fret)

    @property
    def was_within_active_click_zone(self) -> bool:
        """Check if event was within the grid.

        The active click zone is somewhat larger than the grid, because it includes
        the pixels to the top, left and right of the grid where dots would take up soem space."""
        diagram: DataDiagram = self.interface.diagram_collection[0]
        grid_origin = diagram.origin_grid
        x_min = grid_origin.x - diagram.geometry.dot_radius
        x_max = grid_origin.x + diagram.width_grid + diagram.geometry.dot_radius
        y_min = grid_origin.y - diagram.geometry.dot_radius * 2  # Space above the diagram
        y_max = grid_origin.y + diagram.height_grid

        x_bound = x_min < self.event.x < x_max
        y_bound = y_min < self.event.y < y_max
        return x_bound and y_bound

    @property
    def was_near_course(self):
        """Get the course index the user clicked on.

            Returns the index of the course or None if no course was clicked on"""
        if self.was_within_active_click_zone:
            diagram: DataDiagram = self.interface.diagram_collection[0]
            course_origins = diagram.origin_courses
            for index_course, origin in enumerate(course_origins):
                minimum = origin.x - diagram.geometry.dot_radius
                maximum = origin.x + diagram.geometry.dot_radius
                if minimum < self.event.x < maximum:
                    return index_course

    @property
    def was_near_fret(self):
        """Get the fret index the user clicked on.

            Returns the index of the fret or None if no fret was clicked on"""
        if self.was_within_active_click_zone:
            diagram: DataDiagram = self.interface.diagram_collection[0]
            fret_origins = diagram.origin_frets

            # print("Origins: ", [x.y for x in diagram.origin_courses])
            # print("Interval: ", diagram.geometry.interval_course)
            # print("Scaling: ", diagram.geometry.scaling_factor)
            # print("Stroke: ", diagram.courses[0].geometry.stroke)

            for index_fret, origin in enumerate(fret_origins):
                # minimum = origin.y - diagram.diagram_geometry.reference_dot_radius * 2
                # Todo: this isn't right... interval fret doesn't return with the correct value...

                minimum = origin.y - diagram.geometry.interval_fret
                minimum -= diagram.positions[0].geometry.stroke  # fret_stroke + 20

                maximum = origin.y + diagram.positions[0].geometry.stroke

                if minimum < self.event.y < maximum:
                    return index_fret

    @property
    def node_click(self):
        return self.was_near_course, self.was_near_fret
