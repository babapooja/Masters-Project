'''
QUERY:
--------------------------- stackoverflow db -----------------------------------------
    1. '
            for $x in json-lines('collection-faq.json').faqs[]
            return $x.tags[1];

        '
    2. '
            for $question in json-lines('collection-faq.json').faqs[],
                $answer in json-lines('collection-answers.json').answers[]
            where $question.question_id eq $answer.question_id
            return
            {
                "question":$question.title,
                "answer_score":$answer.score
            };

        '
    3. '
            for $question in json-lines('collection-faq.json').faqs[],
                $answer in json-lines('collection-answers.json').answers[]
            where contains($question.title, "MySQL") and
            $question.question_id eq $answer.question_id and
            $question.score gt 4
                
            return
            {
                "question":$question.title,
                "answer_score":$answer.score
            }; 
        '
    4. '
            for $answer in json-lines('collection-answers.json').answers[]
            where $answer.score ge 4
            return $answer.question_id;

        '
    5. '
            for $faq in json-lines('collection-faq.json').faqs[]
            where $faq.title eq "Databases"
            return $faq.tags;

        '
    6. '
            for $question in json-lines('collection-faq.json').faqs[]
            where contains($question.title, "MySQL")
            return
            {
                "question":$question.title
            };

    '
--------------------------- orders db -----------------------------------------
1. Get the names of the customers 
    '
        for $customer in json-lines('customers.json').customers[]
            return $customer.CNAME;
    '
2. Get the names of the customer and the employee who live in the same city
    '
        for $customer in json-lines('customers.json').customers[],
            $employee in json-lines('employees.json').employees[]
        where $customer.CITY eq $employee.CITY
        return {
            "customer_name": $customer.CNAME,
            "employee_name": $employee.ENAME
            };
    '
3. For each customer, find a list of Order Numbers they have placed.
    '
        for $customer in json-lines('customers.json'),
            $order in json-lines('orders.json').orders[]
        where $customer.CNO eq $order.CUSTOMER        
        return {
            "customer_name": $customer.CNAME,
            "customer_number": $customer.CNO,
            "order_number": $order.ONO
        };
    '
4. Get the names of the customers whose address has 'St.' 
    '
        for $customer in json-lines('customers.json').customers[]
        where contains($customer.STREET, "St.")
        return {
            "name": $customer.CNAME,
            "address": $customer.STREET
        };
    '
5. Get the names of customers who have ordered parts only from employees living in 'Wichita'.
    '
        for $customer in json-lines('customers.json').customers[],
	        $employee in json-lines('employees.json'),
	        $order in json-lines('orders.json')
        where $employee.CITY eq "Wichita" and
	          $order.TAKENBY eq $employee.ENO and
	          $order.CUSTOMER eq $customer.CNO
        return {
            "customer_id": $customer.CNO,
            "name": $customer.CNAME
        }
    '
'''