struct Student {
    let name: String
    let scores: [Subject: Int]
}

enum Subject: String, CaseIterable {
    case Chinese, Math, English
}

let s1 = Student(
    name: "Jane",
    scores: [.Chinese: 86, .Math: 92, .English: 73]
)

let s2 = Student(
    name: "Jane",
    scores: [.Chinese: 99, .Math: 52, .English: 97]
)

let s3 = Student(
    name: "Jane",
    scores: [.Chinese: 91, .Math: 92, .English: 100]
)

let students = [s1, s2, s3]

// 检查 students 里的学生的平均分，并输出第一名的姓名。

// 命令式
func bestImperative(students: [Student]) -> String? {
    var best: (Student, Double)?
    
    for s in students {
        var totalScore = 0
        for key in Subject.allCases {
            totalScore += s.scores[key] ?? 0
        }
        
        let averageScore = Double(totalScore) /
            Double(Subject.allCases.count)
        
        if let temp = best {
            if averageScore > temp.1 {
                best = (s, averageScore)
            }
        } else {
            best = (s, averageScore)
        }
    }
    
    print(best?.0.name ?? "no students")
    
    return best?.0.name
}

bestImperative(students: [])
bestImperative(students: students)

// 声明式编程

// 函数式
func average(_ scores: [Subject: Int]) -> Double {
    return Double(scores.values.reduce(0, +)) / Double(Subject.allCases.count)
}

let bestStudent = students
    .map { ($0, average($0.scores)) }
    .sorted { $0.1 > $1.1 }
    .first

// DSL: e.g. SQL
//
//select name, avg(score) as avs_score
//from scores group by name order by avg_score;
