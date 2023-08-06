import variables as v
import functions as f


def run():
    for i in range(v.iterations):
    # while loop:
        v.p, point_list = f.rotate(v.p)
        print(point_list)


run()
