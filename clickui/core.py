import tkinter as tk
import typing
from tkinter import filedialog

import click
import click.core
import tkcalendar as tkc


class TkCommandView:

    def __init__(self, cmd: click.Command, **kwargs):
        """
        Provide views on top of click.Command
        :param cmd:
        :param kwargs:
        """
        self.cmd = cmd
        self.obj_views_list: list = []
        self.arg_views_list: list = []
        self.opt_views_list: list = []
        self.ctx_view: click.Context = None
        self.create_ui()

    def create_ui(self):
        self.app: tk.Tk = tk.Tk()
        obj_list: list = []
        arg_list: list = []
        opt_list: list = []
        ctx: click.Context = None
        for item in self.cmd.params:
            if type(item) == click.core.Argument:
                arg_list.append(item)
            elif type(item) == click.core.Option:
                opt_list.append(item)
            elif isinstance(item) == dict:
                obj_list.append(item)
            else:
                raise TypeError(f'Unknown parameter {item.__class__}')

        self.arg_views_list = [view_mapping[type(argument.type)](argument, self.app) for argument in arg_list]
        self.opt_views_list = [view_mapping[type(option.type)](option, self.app) for option in opt_list]
        self.obj_views_list = [ObjectView(object, self.app) for object in obj_list]
        self.ctx_view = None if not ctx else ContextView(ctx, self.app)

        run_btn: tk.Button = tk.Button(master=self.app, text='Run', command=self.invoke_cmd)
        run_btn.pack(fill=tk.X)

    def invoke_cmd(self):
        param_list: list = []
        for arg in self.arg_views_list:
            param_list = param_list + arg.value()

        for opt in self.opt_views_list:
            param_list = param_list + opt.value()

        try:
            self.cmd.main(args=param_list)
        finally:
            exit(0)

    def __call__(self, *args, **kwargs):
        self.app.mainloop()
        # self.invoke_cmd()
        pass


class ParamView(tk.LabelFrame):
    def __init__(self, param: click.Parameter, master: tk.Tk):
        super().__init__(master, text=param.human_readable_name)
        self.values: list = []
        self.inputs = None
        self.param: click.Parameter = param
        self.create_inputs()
        self.pack(fill=tk.X)

    def create_inputs(self):
        if self.param.multiple:
            self.inputs: typing.List[tk.Widget] = [self.get_input_type()]
        else:
            self.inputs: tk.Widget = self.get_input_type()

    def get_input_type(self):
        if hasattr(self, 'tk_var_type'):
            var = self.tk_var_type()
        else:
            var = tk.StringVar()
        # var: tk.StringVar = tk.StringVar()
        self.values.append(var)
        if hasattr(self, 'tk_input_type'):
            if hasattr(self, 'init_params') and not hasattr(self, 'init_vars'):
                in_put = self.tk_input_type(self, **self.init_params)
            elif not hasattr(self, 'init_params') and hasattr(self, 'init_vars'):
                in_put = self.tk_input_type(self, *self.init_vars)
            elif hasattr(self, 'init_params') and hasattr(self, 'init_vars'):
                in_put = self.tk_input_type(self, *self.init_vars, **self.init_params)
            else:
                in_put = self.tk_input_type(self, variable=var, text=self.param.human_readable_name)
        else:
            in_put = tk.Entry(self, textvariable=var)
        in_put.pack(fill=tk.X)
        return in_put

    def value(self):
        return_list: list = []
        if type(self.inputs) == list:
            for i in self.values:
                if type(self.param) == click.core.Option:
                    return_list.append(self.param.opts[0])
                return_list.append(i.get())
        else:
            if type(self.param) == click.core.Option:
                return_list.append(self.param.opts[0])
            return_list.append(self.values[0].get())
        return return_list


class BoolParamView(ParamView):
    def __init__(self, param: click.Parameter, master: tk.Tk):
        self.tk_input_type = tk.Checkbutton
        self.tk_var_type = tk.BooleanVar
        super().__init__(param, master)

    def value(self):
        return_list: list = []
        if self.param.is_flag and self.values[0].get():
            return_list.append(self.param.opts[0])
        return return_list


class ObjectView(ParamView):

    def __init__(self, obj, master):
        super().__init__(obj, master)


class ContextView(ParamView):

    def __init__(self, ctx, master):
        super().__init__(ctx, master)


class FileParamView(ParamView):
    def __init__(self, param: click.Parameter, master: tk.Tk):
        # Fixme: Find eventbinding for tkinter entry
        # and implement StringVar update on event of
        # Key release or paste
        self.tk_input_type = TkFileSelectorView
        self.tk_var_type = tk.StringVar
        super().__init__(param, master)

    def value(self):
        return_list: list = []
        if type(self.inputs) == list:
            for i in self.values:
                if type(self.param) == click.core.Option:
                    return_list.append(self.param.opts[0])
                return_list.append(i.get())
        else:
            if type(self.param) == click.core.Option:
                return_list.append(self.param.opts[0])
            return_list.append(self.values[0].get())
        return return_list


class TkFileSelectorView(tk.Entry):

    def __init__(self, master=None, variable=None, text='File', btn_text='Browse'):
        # Fixme: Find eventbinding for tkinter entry
        # and implement StringVar update on event of
        # Key release or paste
        super().__init__(master, textvariable=variable, text=text)
        select_btn: tk.Button = tk.Button(master=master, text=btn_text, state=tk.ACTIVE, command=self.set_file)
        select_btn.pack(side='right')
        self.var: tk.StringVar = variable

    def cmd(self):
        print('Hello World')

    def set_file(self):
        file_path: str = filedialog.askopenfilename()
        self.var.set(file_path)
        self.delete(0)
        self.insert(0, file_path)


class TkPathSelectorView(TkFileSelectorView):
    def set_file(self):
        file_path: str = filedialog.askdirectory()
        self.var.set(file_path)
        self.delete(0)
        self.insert(0, file_path)


class PathParamView(FileParamView):
    def __init__(self, param: click.Parameter, master: tk.Tk):
        self.tk_input_type = TkPathSelectorView
        self.tk_var_type = tk.StringVar
        super().__init__(param, master)


class ChoiceView(ParamView):
    def __init__(self, param: click.Parameter, master: tk.Tk):
        self.tk_input_type = tk.OptionMenu
        self.tk_var_type = tk.StringVar
        self.tk_var = tk.StringVar()
        # self.init_params = {
        # }
        self.init_vars = (
            self.tk_var,
            *param.type.choices
        )
        super().__init__(param, master)


class DateTimeView(ParamView):
    def __init__(self, param: click.Parameter, master: tk.Tk):
        self.tk_input_type = tkc.DateEntry
        self.tk_var_type = tk.StringVar
        self.tk_var = tk.StringVar()
        self.init_params = {
            'textvariable' : self.tk_var
        }
        super().__init__(param, master)


class IntView(ParamView):
    def __init__(self, param: click.Parameter, master: tk.Tk):
        self.tk_input_type = tk.Entry
        self.tk_var_type = tk.StringVar
        self.tk_var = tk.StringVar()
        self.init_params = {
            'textvariable' : self.tk_var
        }
        super().__init__(param, master)


class FloatView(ParamView):
    def __init__(self, param: click.Parameter, master: tk.Tk):
        self.tk_input_type = tk.Entry
        self.tk_var_type = tk.StringVar
        self.tk_var = tk.StringVar()
        self.init_params = {
            'textvariable' : self.tk_var
        }
        super().__init__(param, master)


class UuidView(ParamView):
    def __init__(self, param: click.Parameter, master: tk.Tk):
        self.tk_input_type = tk.Entry
        self.tk_var_type = tk.StringVar
        self.tk_var = tk.StringVar()
        self.init_params = {
            'textvariable': self.tk_var
        }
        super().__init__(param, master)


view_mapping: dict = {
    click.types.StringParamType: ParamView,
    click.types.UnprocessedParamType: ParamView,
    click.types.Choice: ChoiceView,
    click.types.DateTime: DateTimeView,
    click.types.IntParamType: IntView,
    click.types.FloatParamType: FloatView,
    click.types.BoolParamType: BoolParamView,
    click.types.UUIDParameterType: UuidView,
    click.types.File: FileParamView,
    click.types.Path: PathParamView,
}
