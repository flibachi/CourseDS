import sys
from analytics import Research
from config import num_of_steps, report_text


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Use: make_report.py <file>")
        sys.exit(1)

    filepath = sys.argv[1]

    try:
        researcher = Research(filepath)
        data = researcher.file_reader(True)

        calculations1 = researcher.Analytics(data)

        heads1, tails1 = calculations1.counts()

        fract1, fract2 = calculations1.fractions(heads1, tails1)

        prediction = calculations1.predict_random(num_of_steps)

        last_prediction = calculations1.predict_last()

        calculations2 = Research.Analytics(prediction)

        heads2, tails2 = calculations2.counts()

        s1 = 's' if tails2 != 1 else ''
        s2 = 's' if heads2 != 1 else ''

        report = report_text.format(
            observations=len(data),
            tails1=tails1,
            heads1=heads1,
            fract_tails1=fract2,
            fract_heads1=fract1,
            num_of_steps=num_of_steps,
            tails2=tails2,
            s1=s1,
            heads2=heads2,
            s2=s2
        )

        calculations1.save_file(report, 'report', 'txt')

    except FileNotFoundError as e:
        print(f"File error: {e}")
        sys.exit(1)

    except ValueError as e:
        print(f"Data error: {e}")
        sys.exit(1)

    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)
