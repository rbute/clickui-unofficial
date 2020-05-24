import tkinter as tk
import typing

import click
import click.core


class CommandView:

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
        self.cmd_view: tk.Frame = None
        self.app: tk.Tk = tk.Tk()
        self.create_ui()
        self.app.mainloop()

    def create_ui(self):
        self.cmd_view = tk.Frame(self.app)
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

        self.arg_views_list = [view_mapping[type(argument.type)](argument, self.cmd_view) for argument in arg_list]
        self.opt_views_list = [view_mapping[type(option.type)](option, self.cmd_view) for option in opt_list]
        self.obj_views_list = [ObjectView(object, self.cmd_view) for object in obj_list]
        self.ctx_view = None if not ctx else ContextView(ctx, self.cmd_view)

        run_btn: tk.Button = tk.Button(master=self.cmd_view, text='Run', command=self.invoke_cmd)
        run_btn.pack(fill=tk.X)
        self.cmd_view.pack()

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


class ParamView(tk.LabelFrame):
    def __init__(self, param: click.Parameter, master: tk.Widget):
        super().__init__(master, text=param.human_readable_name)
        self.param: click.Parameter = param
        self.create_inputs()
        self.pack(fill=tk.X)

    def create_inputs(self):
        if self.param.multiple:
            self.inputs: typing.List[tk.Widget] = [self.get_input_type()]
        else:
            self.inputs: tk.Widget = self.get_input_type()

    def get_input_type(self):
        in_put = tk.Entry(self)
        in_put.pack(fill=tk.X)
        return in_put

    def value(self):
        return_list: list = []
        if type(self.inputs) == list:
            for i in self.inputs:
                if type(self.param) == click.core.Option:
                    return_list.append(self.param.opts[0])
                return_list.append(i.get())
        else:
            if type(self.param) == click.core.Option:
                return_list.append(self.param.opts[0])
            return_list.append(self.inputs.get())
        return return_list


class ObjectView(ParamView):

    def __init__(self, obj, master):
        super().__init__(obj, master)


class ContextView(ParamView):

    def __init__(self, ctx, master):
        super().__init__(ctx, master)


view_mapping: dict = {
    click.types.StringParamType: ParamView,
    click.types.UnprocessedParamType: ParamView,
    click.types.Choice: ParamView,
    click.types.DateTime: ParamView,
    click.types.IntParamType: ParamView,
    click.types.FloatParamType: ParamView,
    click.types.BoolParamType: ParamView,
    click.types.UUIDParameterType: ParamView,
    click.types.File: ParamView,
    click.types.Path: ParamView,
}
