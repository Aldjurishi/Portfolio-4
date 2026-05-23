import math

# ─────────────────────────────────────────────
#  Membership Function Implementations
# ─────────────────────────────────────────────

def get_triangular(x, a, b, c):
    """
    Triangular membership function.
    Shape: rises linearly from a to b, then falls linearly from b to c.
    Parameters: a = start, b = peak, c = end  (must satisfy a < b < c)
    """
    if x <= a or x >= c:
        return 0.0
    elif a < x <= b:
        return (x - a) / (b - a)
    else:
        return (c - x) / (c - b)


def get_trapezoidal(x, a, b, c, d):
    """
    Trapezoidal membership function.
    Shape: rises from a to b, flat top from b to c, falls from c to d.
    Parameters: a = start, b = plateau start, c = plateau end, d = end
    (must satisfy a < b <= c < d)
    """
    if x <= a or x >= d:
        return 0.0
    elif a < x <= b:
        return (x - a) / (b - a)
    elif b < x <= c:
        return 1.0
    else:
        return (d - x) / (d - c)


def get_gaussian(x, c, sigma):
    """
    Gaussian membership function.
    Shape: smooth bell curve centred at c.
    Parameters: c = centre/mean, sigma = standard deviation (must be > 0)
    """
    return math.exp(-0.5 * ((x - c) / sigma) ** 2)


def get_bell_shape(x, a, b, c):
    """
    Generalised Bell membership function.
    Shape: smooth bell, wider and flatter than Gaussian.
    Parameters: a = width (must be > 0), b = slope, c = centre
    """
    return 1.0 / (1.0 + abs((x - c) / a) ** (2 * b))


def get_sigmoid(x, a, c):
    """
    Sigmoid membership function.
    Shape: S-shaped curve, transitions from 0 to 1 around point c.
    Parameters: a = slope (positive = left-to-right rise), c = crossover point
    """
    try:
        return 1.0 / (1.0 + math.exp(-a * (x - c)))
    except OverflowError:
        return 0.0 if a * (x - c) < 0 else 1.0


# ─────────────────────────────────────────────
#  Input Helpers
# ─────────────────────────────────────────────

def get_float(prompt):
    """Repeatedly prompt until a valid float is entered."""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("  Invalid input — please enter a numeric value.")


def validate_params(params, conditions, messages):
    """
    Check a list of conditions on params.
    Returns (True, '') if all pass, or (False, error_message) on first failure.
    """
    for condition, message in zip(conditions, messages):
        if not condition:
            return False, message
    return True, ""


# ─────────────────────────────────────────────
#  Main Program
# ─────────────────────────────────────────────

MENU = """
  1. Triangular
  2. Trapezoidal
  3. Gaussian
  4. Bell Shape
  5. Sigmoid
  6. Change variable name
  7. Exit
"""

def main():
    print("=" * 50)
    print("   Fuzzy Membership Degree Calculator")
    print("=" * 50)

    var_name = input("\nEnter the name of the fuzzy variable (e.g. Temperature): ").strip()
    if not var_name:
        var_name = "Variable"

    while True:
        print(f"\nFuzzy variable : '{var_name}'")
        print("Select a membership function type:")
        print(MENU)

        choice = input("Choice (1-7): ").strip()

        if choice == "7":
            print("\nGoodbye!")
            break

        if choice == "6":
            var_name = input("Enter new variable name: ").strip() or var_name
            continue

        if choice not in ("1", "2", "3", "4", "5"):
            print("  Please enter a number between 1 and 7.")
            continue

        # ── Crisp input ──────────────────────────────
        x = get_float(f"\nEnter the crisp input value for '{var_name}': ")

        # ── Parameters & computation ─────────────────
        result = None

        if choice == "1":
            print("\n  Triangular — define the shape with three points:")
            print("    a = where membership starts rising  (left foot)")
            print("    b = the peak (membership = 1.0)")
            print("    c = where membership finishes falling (right foot)")
            a = get_float("  Enter a (left foot)  : ")
            b = get_float("  Enter b (peak)        : ")
            c = get_float("  Enter c (right foot)  : ")
            ok, msg = validate_params(
                [a, b, c],
                [a < b, b < c],
                ["  Error: a must be less than b.", "  Error: b must be less than c."]
            )
            if not ok:
                print(msg)
                continue
            result = get_triangular(x, a, b, c)

        elif choice == "2":
            print("\n  Trapezoidal — define the shape with four points:")
            print("    a = where membership starts rising  (left foot)")
            print("    b = where the flat top begins")
            print("    c = where the flat top ends")
            print("    d = where membership finishes falling (right foot)")
            a = get_float("  Enter a (left foot)       : ")
            b = get_float("  Enter b (plateau start)   : ")
            c = get_float("  Enter c (plateau end)     : ")
            d = get_float("  Enter d (right foot)      : ")
            ok, msg = validate_params(
                [a, b, c, d],
                [a < b, b <= c, c < d],
                [
                    "  Error: a must be less than b.",
                    "  Error: b must be less than or equal to c.",
                    "  Error: c must be less than d."
                ]
            )
            if not ok:
                print(msg)
                continue
            result = get_trapezoidal(x, a, b, c, d)

        elif choice == "3":
            print("\n  Gaussian — smooth bell curve:")
            print("    c     = centre of the curve (peak)")
            print("    sigma = spread / standard deviation (must be > 0)")
            c     = get_float("  Enter c (centre) : ")
            sigma = get_float("  Enter sigma      : ")
            if sigma <= 0:
                print("  Error: sigma must be greater than 0.")
                continue
            result = get_gaussian(x, c, sigma)

        elif choice == "4":
            print("\n  Bell Shape — generalised bell curve:")
            print("    a = width of the bell  (must be > 0)")
            print("    b = slope of the sides")
            print("    c = centre of the bell")
            a = get_float("  Enter a (width)  : ")
            b = get_float("  Enter b (slope)  : ")
            c = get_float("  Enter c (centre) : ")
            if a <= 0:
                print("  Error: a must be greater than 0.")
                continue
            result = get_bell_shape(x, a, b, c)

        elif choice == "5":
            print("\n  Sigmoid — S-shaped transition:")
            print("    a = slope  (positive = rises left to right, negative = falls)")
            print("    c = crossover point where membership = 0.5")
            a = get_float("  Enter a (slope)      : ")
            c = get_float("  Enter c (crossover)  : ")
            result = get_sigmoid(x, a, c)

        # ── Output ───────────────────────────────────
        if result is not None:
            result = max(0.0, min(1.0, result))   # clamp to [0, 1]
            bar_len = int(result * 30)
            bar = "█" * bar_len + "░" * (30 - bar_len)

            print(f"\n  ┌─ Result for '{var_name}' ─────────────────────")
            print(f"  │  Crisp input value   : {x}")
            print(f"  │  Membership degree   : {result:.4f}")
            print(f"  │  [{bar}] {result * 100:.1f}%")
            print(f"  └────────────────────────────────────────────")


if __name__ == "__main__":
    main()
