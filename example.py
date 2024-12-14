from cli import CLI

cli = CLI()

cli.addItem("Say \"Hello, World\"!")

def sayHelloWorld():
    cli.print("Hello, World!")

cli.addFunction(idx=0, func=sayHelloWorld, args=())

cli.addItem("/f red/Coloured /f green/Item/reset/!")

def colouredResponse():
    cli.print("Wow!")

cli.addFunction(idx=1, func=colouredResponse, args=())

cli.run()
