from z3 import *
import json

def sweetbrier_circuit_breaker(llm_intent_json):
    intent = json.loads(llm_intent_json)
    solver = Solver()
    
    financial_extraction = Bool('financial_extraction')
    unauthorized_data_transfer = Bool('unauthorized_data_transfer')
    harm_to_user = Bool('harm_to_user')
    execution_approved = Bool('execution_approved')
    
    solver.add(Implies(financial_extraction == True, execution_approved == False))
    solver.add(Implies(unauthorized_data_transfer == True, execution_approved == False))
    solver.add(Implies(harm_to_user == True, execution_approved == False))
    
    solver.add(Implies(And(financial_extraction == False, 
                           unauthorized_data_transfer == False, 
                           harm_to_user == False), 
                       execution_approved == True))
    
    solver.add(financial_extraction == intent.get("financial_extraction", False))
    solver.add(unauthorized_data_transfer == intent.get("unauthorized_data_transfer", False))
    solver.add(harm_to_user == intent.get("harm_to_user", False))
    
    if solver.check() == sat:
        model = solver.model()
        return is_true(model[execution_approved])
    return False

# Minimal verification check
test_pass = json.dumps({"action": "read", "financial_extraction": False, "unauthorized_data_transfer": False, "harm_to_user": False})
test_fail = json.dumps({"action": "extract", "financial_extraction": True, "unauthorized_data_transfer": False, "harm_to_user": False})

print(f"Pass check approved: {sweetbrier_circuit_breaker(test_pass)}")
print(f"Fail check approved: {sweetbrier_circuit_breaker(test_fail)}")