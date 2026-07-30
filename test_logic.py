def calculate(ratio, rotate):
    # final container
    print("final ratio:", ratio)
    # inner view
    inner = 1.0/ratio if rotate in [90, 270] else ratio
    print("inner ratio:", inner)

calculate(16/9.0, 90)
