from cli import CLI

cli = CLI()

cli.addItem("Say \"Hello, World\"!")

def sayHelloWorld():
    cli.print("Hello, World!")

cli.addFunction(idx=0, func=sayHelloWorld, args=())

cli.run()
