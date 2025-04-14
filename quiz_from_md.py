import re

def load_questions(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()

    questions = []
    current = []

    for line in lines:
        line = line.strip()
        if line.startswith('###'):
            if current:
                questions.append(current)
                current = []
        current.append(line)
        if '**[⬆ Back to Top]' in line:
            questions.append(current)
            current = []

    return [q for q in questions if any(opt_line.startswith('- [') for opt_line in q)]

def parse_question(block):
    question_text = ''
    options = []
    correct_indexes = []

    for line in block:
        if line.startswith('###'):
            question_text = line[4:].strip()
        elif line.startswith('- ['):
            match = re.match(r'- \[( |x)\] (.+)', line)
            if match:
                checked, text = match.groups()
                options.append(text)
                if checked == 'x':
                    correct_indexes.append(len(options) - 1)

    if not question_text:
        question_text = next((l for l in block if l and not l.startswith('- [')), '(Missing question text)')

    return question_text, options, correct_indexes

def parse_user_input(raw_input):
    # Accept 2 5 or 2,5 or 2;5 or any mix
    parts = re.split(r'[,\s;]+', raw_input.strip())
    try:
        return sorted(set(int(x) - 1 for x in parts if x.isdigit()))
    except Exception:
        return []

def run_quiz(filename):
    questions = load_questions(filename)
    score = 0

    for i, q_block in enumerate(questions):
        question, options, correct_indexes = parse_question(q_block)

        if not options:
            print(f'\n⚠️ Skipping question {i + 1} — no valid options found.')
            continue

        print(f'\nQuestion {i + 1}: {question}')
        for idx, opt in enumerate(options):
            print(f'  {idx + 1}. {opt}')

        raw_input_str = input('Your answer (e.g. 2,5 or 1 3): ')
        selected_indexes = parse_user_input(raw_input_str)

        if not selected_indexes:
            print('⚠️ Invalid input, skipping question.')
            continue

        if sorted(selected_indexes) == sorted(correct_indexes):
            print('✅ Correct!')
            score += 1
        else:
            correct_str = ', '.join(str(i + 1) for i in correct_indexes)
            print(f'❌ Incorrect. Correct answer(s): {correct_str}')

    print(f'\n🏁 Quiz complete! Score: {score}/{len(questions)}')

if __name__ == '__main__':
    run_quiz('Practice-questions.md')

