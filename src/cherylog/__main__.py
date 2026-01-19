from cherylog.bootstrap import Container, Bootstrapper

container = Container()
bootstrapper = Bootstrapper(container)

def main():
    bootstrapper.run()

if __name__ == '__main__':
    main()