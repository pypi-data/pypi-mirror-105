import runpy


def main():
    my_package = runpy.run_module(
        mod_name="src.ops", init_globals=globals())
    my_package['main']()


if __name__ == "__main__":
    main()
