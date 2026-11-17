def in_language(word):
    """Return True exactly when word is a^n b^n for some n >= 0."""
    split = 0
    while split < len(word) and word[split] == "a":
        split += 1
    return all(symbol == "b" for symbol in word[split:]) and split == len(word) - split


def simulate(p):
    """Audit every legal split of w = a^p b^p, pumping down with i = 0."""
    if not isinstance(p, int) or isinstance(p, bool) or p < 1:
        raise ValueError("p must be a positive integer")

    w = "a" * p + "b" * p
    audits = []
    for x_length in range(p):
        for y_length in range(1, p - x_length + 1):
            z_a_length = p - x_length - y_length
            x = "a" * x_length
            y = "a" * y_length
            z = "a" * z_a_length + "b" * p
            pumped = x + z  # x y^0 z = xz
            a_count = pumped.count("a")
            b_count = pumped.count("b")
            member = in_language(pumped)
            audits.append({
                "x": x, "y": y, "z": z, "pumped": pumped,
                "x_length": x_length, "y_length": y_length,
                "z_length": len(z), "a_count": a_count,
                "b_count": b_count, "in_language": member,
            })

    expected = p * (p + 1) // 2
    assert len(audits) == expected, "Not every legal split was audited"
    assert all(not row["in_language"] for row in audits), "A split did not violate membership"
    return w, audits


def main():
    p = int(input("Enter the proposed pumping length p: "))
    w, audits = simulate(p)
    print(f"Witness w = {w} (length {len(w)})")
    print(f"Legal splits checked: {len(audits)}")
    for index, row in enumerate(audits, start=1):
        result = "IN L" if row["in_language"] else "OUT OF L"
        print(
            f"{index}: x={row['x']!r}, y={row['y']!r}, z={row['z']!r}; "
            f"i=0 gives xz={row['pumped']!r}; "
            f"a={row['a_count']}, b={row['b_count']} -> {result}"
        )
    print("Conclusion: every legal split fails after pumping down with i=0.")


if __name__ == "__main__":
    main()