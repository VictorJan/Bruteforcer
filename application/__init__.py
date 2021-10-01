from application.utils.design.application.builder import ApplicationBuilder
from application.tool import EnumeratorTool,TimeItToolDecorator

builder=ApplicationBuilder()
builder.tool=TimeItToolDecorator(EnumeratorTool())
product=builder.product