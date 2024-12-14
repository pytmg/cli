from cli import CLI

cli = CLI()

cli.addItem("Say \"Hello, World\"!")

def sayHelloWorld():
    cli.print("Hello, World!")

cli.addFunction(0, sayHelloWorld, ())

cli.addItem("/f red/Coloured /f green/Item/reset/!")

def colouredResponse():
    cli.print("Wow!")

cli.addFunction(1, colouredResponse, ())

cli.run()
