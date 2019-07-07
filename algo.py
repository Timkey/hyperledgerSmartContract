import time

class bonusContract():

	def __init__(self):
		
		#load list of beneficiaries {"address":'hash', "employeeCode":03245, "amount":4000}
		self.beneficiaries = [{"address":'hash', "employeeCode":"03245", "amount":4000}]

		#load list of partners and associatons to beneficiary {"address":'hash', "benefactor":"employeeCode=03245", "portion":"20%"}
		self.partners = [{"address":'hash1', "benefactor":"03245", "portion":20}]

		#load list of approved companies fetch data from an oracle confirming validity of the company {"companyName":"Amazon", "categoty":"Shopping"}
		self.validCompanies = [{"companyName":"Amazon", "categoty":"Shopping"}]

		#load list of expenditures {"address":"hash", "amount":"2000", "timestamp":time.time(), "where":"company"}
		self.expenditure = [{"address":"hash", "amount":1000, "timestamp":time.time(), "where":"Amazon"},{"address":"hash1", "amount":100, "timestamp":time.time(), "where":"Amazon"}]
		
	def execContract(self, byWho, toCompany, payOutAmount):

		#is company valid
		if self.verifyCompany(toCompany) == True:
			
			# is beneficiary valid
			response = self.verifyBeneficiary(byWho)
			#print response, '<=benef'
			if response == False:

				#check if partner instead
				response = self.verifyPartner(byWho)
				#rint response, '<=partner'

				if response == False:

					# terminate process : beneficiary not valid
					return False

				else:

					#compute expense
					return self.updateExpense(byWho, payOutAmount, toCompany, response)

			else:

				#update expense
				return self.updateExpense(byWho, payOutAmount, toCompany, response)

		else:

			#terminate process : Invalid company
			return False

	def verifyCompany(self, toCompany):

		#search for approval
		response = False

		for each in self.validCompanies:

			if toCompany in each['companyName']:

				#update found
				response = True
				break
			
		#express decision
		return response

	def verifyBeneficiary(self, byWho):

		#default response
		response = False

		for stack in self.beneficiaries:
		
			#check if in list
			if byWho in stack['address']:

				#get staff employeeCode
				empCode = 0
				amount = 0
				for each in self.beneficiaries:

					if each['address'] == byWho:

						amount = each['amount']
						empCode = each['employeeCode']

				#check if beneficiary has partners
				#get amount benefactor gave partners
				partner = 0

				for each in self.partners:

					if each['benefactor'] == empCode:
						
						allot = each['portion']

						#compute amount
						partner = partner + (amount*(allot/100))

				#compute how much benefactor has spent
				
				expense = 0
				for each in self.expenditure:

					if byWho in each['address']:

						#get expenses
						expense = expense + each['amount']

				# how much is benefactor left with
				response = amount - partner - expense
				break

		#results
		return response

	def verifyPartner(self, byWho):

		#default setup for response
		response = False

		#search beneficiary
		for each in self.partners:

			#partner portion and benefactor
			if byWho in each['address']:

				#found, extract info and exit
				benefactor = each['benefactor']
				portion = each['portion']
				break

		if 'benefactor' in locals():

			#find expenses and alloted portion
			#alloted amount

			for each in self.beneficiaries:

				#filter by employeeCode
				if benefactor in each['employeeCode']:

					#get amount : there could be more than one benefactor dont break
					alloted = each['amount']*(portion/100)

			#does alloted exist: find expenses
			if 'alloted' in locals():

				#expenses
				totExp = 0
				for each in self.expenditure:

					#filter by address
					if byWho in each['address']:

						#sum expense
						totExp = totExp + each['amount']

				#update remainder
				response = alloted - totExp

		#reporting results
		return response

	def updateExpense(self, byWho, amount, toCompany, inStore):

		#init respone
		respone = False

		#check if balance is positive
		if (inStore - amount) > -1:

			#update
			self.expenditure.append({"address":byWho, "amount":amount, "timestamp":time.time(), "where":toCompany})
			respone = True

		#terminate
		return respone

#testing phase
'''
cont = bonusContract()
print cont.execContract('hash1', 'Amazon', 500)
'''