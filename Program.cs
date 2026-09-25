//Console.WriteLine("Банковский счёт");

//double balance = 1000;
//Console.WriteLine($"Начальный баланс {balance}");

//balance += 500;
//Console.WriteLine($"После пополнения на 500: {balance}");

//balance -= 200;
//Console.WriteLine($"После покупки на 200: {balance}");

//balance *= 1.05; // начисление 5% процентов 
//Console.WriteLine($"После начисления 5%: {balance}");

//balance /= 2; // разделили счёт на пополам с партнёром
//Console.WriteLine($"После деления пополам: {balance}");

//Console.WriteLine();
//Console.WriteLine("Постфикс vs префикс");
//
//int lessonNumber = 1;
//Console.WriteLine($"lessonNumber++ выводит:  {lessonNumber++}");
//Console.WriteLine($"После этого lessonNumber = {lessonNumber}");
//
//int weekNumber = 1;
//Console.WriteLine($"++weekNumber выводит: {++weekNumber}");
//Console.WriteLine($"После этого weekNumber = {weekNumber}");
//
//Console.WriteLine();
//Console.WriteLine("Практическая ловушка");
//
//int attempts = 0;
//Console.WriteLine($"Попытка №{++attempts}");
//Console.WriteLine($"Попытка №{++attempts}");
//Console.WriteLine($"Всего попыток: {attempts}");
//
//Console.WriteLine();
//Console.WriteLine("Операторы сравнения");

//double myGrade = 4.6;
//double passingGrade = 4.0;
//int myAge = 20;
//int votingAge = 18;
//
//bool isPassing = myGrade >= passingGrade;
//bool isExactAge = myAge == votingAge;
//bool canVote = myAge >= votingAge;
//bool isNotFailing = myGrade != 2.0; vb 
//Console.WriteLine($"Балл {myGrade} >= {passingGrade}: {isPassing}");
//Console.WriteLine($"Возраст {myAge} == {votingAge}: {isExactAge}");
//Console.WriteLine($"Возраст {myAge} >= {votingAge}(может голосовать): {canVote}");
//Console.WriteLine($"Балл {myGrade} != 2.0 (не двойка): {isNotFailing}");

//Console.WriteLine();
//Console.WriteLine("Логические операторы");
//
//bool hasPassingGrade = true;
//bool hasAttendance = false;
//bool hasDebt = true;
//
//bool canGetScholarship = hasPassingGrade && hasAttendance;
//bool canRetakeExam = hasPassingGrade || hasAttendance;
//bool isDebtFree = !hasDebt;
//
//Console.WriteLine($"Может получить стипендию (оценка И посещаемость):{canGetScholarship}");
//Console.WriteLine($"Может пересдать (оценка ИЛИ посещаемость) {canRetakeExam}");
//Console.WriteLine($"Нет долгов: {isDebtFree}");


Console.WriteLine();
Console.WriteLine("Короткое замыкание");

bool CheckAndPrint (string label, bool value) {
    Console.WriteLine($"   Вычисляется: {label}");
    return value;
}

Console.WriteLine("Проверяем && (первый опернад false):");
bool resultAnd = CheckAndPrint("A", false) && CheckAndPrint("B", true);
Console.WriteLine($"Результат:{resultAnd}");

Console.WriteLine();
Console.WriteLine("Проверяем || (первый операнл true):");
bool resultOr = CheckAndPrint("C",true) || CheckAndPrint("D",false);
Console.WriteLine($"Результат:{resultOr}");