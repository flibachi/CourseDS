import sys
from analytics import Research
from config import report_text, num_of_steps, logging


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Use: make_report.py <file>")
        logging.error('Argument failed')
        sys.exit(1)

    filepath = sys.argv[1]
    report_success = False

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
        report_success = True

    except FileNotFoundError as e:
        logging.error(f"File error: {e}")

    except ValueError as e:
        logging.error(f"Data error: {e}")

    except Exception as e:
        logging.error(f"Unexpected error: {e}")

    finally:
        try:
            researcher.send_message_to_bot(report_success)
            logging.info("Program execution completed")
        except Exception as telegram_error:
            raise (f"Telegram error: {telegram_error}")
