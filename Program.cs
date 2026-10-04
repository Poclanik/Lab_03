using System;
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

//
//Console.WriteLine();
//Console.WriteLine("Короткое замыкание");
//
//bool CheckAndPrint (string label, bool value) {
//    Console.WriteLine($"   Вычисляется: {label}");
//    return value;
//}
//
//Console.WriteLine("Проверяем && (первый опернад false):");
//bool resultAnd = CheckAndPrint("A", false) && CheckAndPrint("B", true);
//Console.WriteLine($"Результат:{resultAnd}");
//
//Console.WriteLine();
//Console.WriteLine("Проверяем || (первый операнл true):");
//bool resultOr = CheckAndPrint("C",true) || CheckAndPrint("D",false);
//Console.WriteLine($"Результат:{resultOr}");

//Console.WriteLine();
//Console.WriteLine("Приоритет операций");
//
//int resultNoParens = 2 + 3 * 4;
//int resultWithParens = (2 + 3) * 4; 
//Console.WriteLine($"2 + 3 * 4   = {resultNoParens}");
//Console.WriteLine($"(2 + 3) * 4   = {resultWithParens}");
//
//bool logicResult = 5 > 3 && 2 < 4 || false;
//bool logicResultParens = (5 > 3 && 2 < 4) || false;
//
//Console.WriteLine($"5 > 3 && 2 < 4 || false = {logicResult}");
//Console.WriteLine($"(5 > 3 && 2 < 4) || false = {logicResultParens}");

//Console.WriteLine();
//Console.WriteLine("Приёмная комиссия");
//
//Console.WriteLine("Введите средний балл аттестата:");
//double averageGrade = double.Parse(Console.ReadLine());
//
//Console.Write("Введите баллы за экзамен (0-100):");
//int examCore = int.Parse(Console.ReadLine());
//
//Console.Write("Есть льгота? (1 - да, 0 - нет): ");
//int beneffitInput = int.Parse(Console.ReadLine());
//bool hasBenefit = (beneffitInput == 1);
//
//bool hasGoodCertificate = averageGrade >= 4.0 ? true : false;
//
//bool hasGoodExam = examCore >= 60 ? true : false;
//
//bool isEligibleByRules = (hasGoodCertificate && hasGoodExam) || hasBenefit ? true : false;
//
//double totalScore = averageGrade * 10;
//totalScore += examCore;
//
//Console.WriteLine();
//Console.WriteLine("Результат");
//Console.WriteLine($"Хороший аттестат (>= 4.0): {hasGoodCertificate}");
//Console.WriteLine($"Хороший экзамен(>=60): {hasGoodExam}");
//Console.WriteLine($"Льгота: {hasBenefit}");
//Console.WriteLine($"Проходит по правилам: {isEligibleByRules}");
//Console.WriteLine($"Итоговый балл: {totalScore}");

//*
//int vvod = int.Parse(Console.ReadLine());
//bool isEven = (vvod % 2) == 0 ? true : false;
//Console.WriteLine(isEven);

////**
//int a = 5;
//int result1 = a++; 
////Сначала значение 5 записывается в result1, и только потом a становится 6.
////Итог: result1 = 5, a = 6
//int b = 5;
//int result2 = ++b; 
//// Сначала b увеличивается до 6, и уже это новое значение 6 записывается в result2.
//// Итог: result2 = 6, b = 6
//int x = 10;
//int math1 = 2 * x++; 
////Для умножения берем старое значение x (10). 2 * 10 = 20. После этого x становится 11.
////Итог: math1 = 20, x = 11
//int y = 10;
//int math2 = 2 * ++y; 
////Сначала y увеличивается до 11, а потом участвует в умножении. 2 * 11 = 22.
////Итог: math2 = 22, y = 11
//int m = 100;
//Console.WriteLine($"Постфикс: {m++}"); 
////В строку подставляется текущее значение 100. Увеличение до 101 происходит уже после вывода.
//int n = 100;
//Console.WriteLine($"Префикс: {++n}");  
////Сначала n становится 101, и именно 101 выводится на экран.
Console.Write("Введите сумму покупки: ");
double Summa = double.Parse(Console.ReadLine());
Console.Write("Введите 1 - есть карта постоянного клиента, 0 - нет: ");
int vvod = int.Parse(Console.ReadLine());
bool cardHav = vvod == 1;
Console.Write("Введите количество товаров в чеке: ");
int kolvo = int.Parse(Console.ReadLine());
bool eligibleForDiscount = (Summa >= 3000 && kolvo >= 3) || cardHav;
Console.WriteLine($"Право на скидку {eligibleForDiscount}");

