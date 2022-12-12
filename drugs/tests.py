import random
from django.test import TestCase
from .models import Drug, Tablet, Suspension, Injectable, Sale

# Create your tests here.
# # Add units to sales!!!!!!!!!!!!!!!!!!!!!!!!


# create tablet

# add tablet
	# check price

# sell tablet
class TestDrugs(TestCase):
	def create_drug():
		_drug = Drug(
					drug_name="Drug1",
					brand_name="brand1",
					drug_type="type1",
					state="",
					weight=100,
					manufacturer="manufacturer1",
					exp_date="2023-10-12",
					purchase_amount=10,
					units="",
					price=100,
					category="category1",
					purpose="purpose1",
					location="location1",
					)
		return _drug

class TabletModelTests(TestCase):
	
	def test_create_tablet_unit(self):
		drug = TestDrugs.create_drug()
		drug.drug_name = "unit"
		drug.state = "Tablet"
		drug.units = "Unit"
		tablet = Tablet(
			drug=drug,
			tab_cd="10/5",
			no_packs=20,
			)
		tablet.save()
		n_tabs = int(tablet.get_tab_cd()[0])
		self.assertEqual(tablet.drug.price, 10)
		self.assertEqual(tablet.drug.stock_amount, tablet.drug.purchase_amount * n_tabs)
  
		sale_amount = random.randint(1, tablet.drug.purchase_amount)
		tablet.sell(sale_amount)
		self.assertEqual(tablet.drug.stock_amount, (tablet.drug.purchase_amount - sale_amount) * n_tabs)
  
		update_amount = random.randint(1, tablet.drug.purchase_amount)
		price=random.randint(1, int(drug.price))
		old_amount = tablet.drug.stock_amount
		tablet.update_stock(update_amount, units=drug.units, price=price)
		self.assertEqual(tablet.drug.price, price/update_amount)
		self.assertEqual(tablet.drug.stock_amount, old_amount + (update_amount * n_tabs))
  

	def test_create_tablet_packet(self):
		drug = TestDrugs.create_drug()
		drug.state = "Tablet"
		drug.units = "Packets"
		tablet = Tablet(
			drug=drug,
			tab_cd="10/5",
			no_packs=20,
			)
		tablet.save()
		n_tabs, n_cards = [int(i) for i in tablet.get_tab_cd()]
		self.assertEqual(tablet.drug.price, 2)
		self.assertEqual(tablet.drug.stock_amount, tablet.drug.purchase_amount * n_cards * n_tabs)
		sale_amount = random.randint(1, tablet.drug.purchase_amount)
		tablet.sell(sale_amount, units=drug.units)
		self.assertEqual(tablet.drug.stock_amount, (tablet.drug.purchase_amount - sale_amount) * n_cards * n_tabs)
  
		update_amount = random.randint(1, tablet.drug.purchase_amount)
		price=random.randint(1, int(drug.price))
		old_amount = tablet.drug.stock_amount
		tablet.update_stock(update_amount, units=drug.units, price=price)
		self.assertEqual(tablet.drug.price, price / update_amount / n_cards)
		self.assertEqual(tablet.drug.stock_amount, old_amount + (update_amount * n_tabs * n_cards))

	def test_create_tablet_carton(self):
		drug = TestDrugs.create_drug()
		drug.state = "Tablet"
		drug.units = "Cartons"
		tablet = Tablet(
			drug=drug,
			tab_cd="10/5",
			no_packs=2,
			)
		tablet.save()
		n_tabs, n_cards = [int(i) for i in tablet.get_tab_cd()]
		self.assertEqual(tablet.drug.price, 1)
		self.assertEqual(tablet.drug.stock_amount, tablet.drug.purchase_amount * n_cards * n_tabs * 2)
		sale_amount = random.randint(1, tablet.drug.purchase_amount)
		tablet.sell(sale_amount, units=drug.units)
		self.assertEqual(tablet.drug.stock_amount, (tablet.drug.purchase_amount - sale_amount) * n_cards * n_tabs * 2)
  
		update_amount = random.randint(1, tablet.drug.purchase_amount)
		price=random.randint(1, int(drug.price))
		old_amount = tablet.drug.stock_amount
		tablet.update_stock(update_amount, units=drug.units, price=price)
		self.assertEqual(tablet.drug.price, price / update_amount / tablet.no_packs / n_cards)
		self.assertEqual(tablet.drug.stock_amount, old_amount + (update_amount * n_tabs * n_cards * tablet.no_packs))

# create suspension

# add suspension

# sell suspension

class SuspensionModelTests(TestCase):
	
	def test_suspension_unit(self):
		drug = TestDrugs.create_drug()
		drug.drug_name = "unit"
		drug.state = "Suspension"
		drug.units = "Unit"
		suspension = Suspension(
			drug=drug,
			no_bottles=12,
			no_packs=20,
			)
		suspension.save()
		
		self.assertEqual(suspension.drug.price, (100 / suspension.drug.purchase_amount))
		self.assertEqual(suspension.drug.stock_amount, suspension.drug.purchase_amount)
  
		sale_amount = random.randint(1, suspension.drug.purchase_amount)
		suspension.sell(sale_amount)
		self.assertEqual(suspension.drug.stock_amount, (suspension.drug.purchase_amount - sale_amount))
  
		update_amount = random.randint(1, suspension.drug.purchase_amount)
		price=random.randint(1, int(drug.price))
		old_amount = suspension.drug.stock_amount
		suspension.update_stock(update_amount, units=drug.units, price=price)
		self.assertEqual(suspension.drug.price, price/update_amount)
		self.assertEqual(suspension.drug.stock_amount, old_amount + update_amount)
  

	def test_suspension_packet(self):
		drug = TestDrugs.create_drug()
		drug.state = "Suspension"
		drug.units = "Packets"
		drug.price = 150
		suspension = Suspension(
			drug=drug,
			no_bottles=12,
			no_packs=20,
			)
		suspension.save()
		print("test-p ", suspension.drug.price)
		self.assertEqual(suspension.drug.price, (150 / suspension.drug.purchase_amount / suspension.no_bottles))
		self.assertEqual(suspension.drug.stock_amount, (suspension.drug.purchase_amount * suspension.no_bottles))
		sale_amount = random.randint(1, suspension.drug.purchase_amount)
		suspension.sell(sale_amount, units=drug.units)
		self.assertEqual(suspension.drug.stock_amount, (suspension.drug.purchase_amount - sale_amount) * suspension.no_bottles)
  
		update_amount = random.randint(1, suspension.drug.purchase_amount)
		price=random.randint(1, int(drug.price))
		old_amount = suspension.drug.stock_amount
		suspension.update_stock(update_amount, units=drug.units, price=price)
		self.assertEqual(suspension.drug.price, price / update_amount / suspension.no_bottles)
		self.assertEqual(suspension.drug.stock_amount, old_amount + (update_amount * suspension.no_bottles))

	def test_suspension_carton(self):
		drug = TestDrugs.create_drug()
		drug.state = "Suspension"
		drug.units = "Cartons"
		drug.price = 12000
		suspension = Suspension(
			drug=drug,
			no_bottles=12,
			no_packs=2,
			)
		suspension.save()
		self.assertEqual(suspension.drug.price, (12000 / suspension.drug.purchase_amount / suspension.no_packs / suspension.no_bottles))
		self.assertEqual(suspension.drug.stock_amount, (suspension.drug.purchase_amount * suspension.no_packs * suspension.no_bottles))
		sale_amount = random.randint(1, suspension.drug.purchase_amount)
		suspension.sell(sale_amount, units=drug.units)
		self.assertEqual(suspension.drug.stock_amount, (suspension.drug.purchase_amount - sale_amount) * suspension.no_packs * suspension.no_bottles)
  
		update_amount = random.randint(1, suspension.drug.purchase_amount)
		price=random.randint(1, int(drug.price))
		old_amount = suspension.drug.stock_amount
		suspension.update_stock(update_amount, units=drug.units, price=price)
		self.assertEqual(suspension.drug.price, price / update_amount / suspension.no_packs / suspension.no_bottles)
		self.assertEqual(suspension.drug.stock_amount, old_amount + (update_amount * suspension.no_packs * suspension.no_bottles))




# create injectable

# add injectable

# sell injectable

# Sale


class InjectableModelTests(TestCase):
	
	def test_injectable_unit(self):
		drug = TestDrugs.create_drug()
		drug.drug_name = "unit"
		drug.state = "Injectable"
		drug.units = "Unit"
		injectable = Injectable(
			drug=drug,
			no_bottles=12,
			no_packs=20,
			)
		injectable.save()
		
		self.assertEqual(injectable.drug.price, (100 / injectable.drug.purchase_amount))
		self.assertEqual(injectable.drug.stock_amount, injectable.drug.purchase_amount)
  
		sale_amount = random.randint(1, injectable.drug.purchase_amount)
		injectable.sell(sale_amount)
		self.assertEqual(injectable.drug.stock_amount, (injectable.drug.purchase_amount - sale_amount))
  
		update_amount = random.randint(1, injectable.drug.purchase_amount)
		price=random.randint(1, int(drug.price))
		old_amount = injectable.drug.stock_amount
		injectable.update_stock(update_amount, units=drug.units, price=price)
		self.assertEqual(injectable.drug.price, price/update_amount)
		self.assertEqual(injectable.drug.stock_amount, old_amount + update_amount)
  

	def test_injectable_packet(self):
		drug = TestDrugs.create_drug()
		drug.state = "Injectable"
		drug.units = "Packets"
		drug.price = 150
		injectable = Injectable(
			drug=drug,
			no_bottles=12,
			no_packs=20,
			)
		injectable.save()
		print("test-p ", injectable.drug.price)
		self.assertEqual(injectable.drug.price, (150 / injectable.drug.purchase_amount / injectable.no_bottles))
		self.assertEqual(injectable.drug.stock_amount, (injectable.drug.purchase_amount * injectable.no_bottles))
		sale_amount = random.randint(1, injectable.drug.purchase_amount)
		injectable.sell(sale_amount, units=drug.units)
		self.assertEqual(injectable.drug.stock_amount, (injectable.drug.purchase_amount - sale_amount) * injectable.no_bottles)
  
		update_amount = random.randint(1, injectable.drug.purchase_amount)
		price=random.randint(1, int(drug.price))
		old_amount = injectable.drug.stock_amount
		injectable.update_stock(update_amount, units=drug.units, price=price)
		self.assertEqual(injectable.drug.price, price / update_amount / injectable.no_bottles)
		self.assertEqual(injectable.drug.stock_amount, old_amount + (update_amount * injectable.no_bottles))

	def test_injectable_carton(self):
		drug = TestDrugs.create_drug()
		drug.state = "Injectable"
		drug.units = "Cartons"
		drug.price = 12000
		injectable = Injectable(
			drug=drug,
			no_bottles=12,
			no_packs=2,
			)
		injectable.save()
		self.assertEqual(injectable.drug.price, (12000 / injectable.drug.purchase_amount / injectable.no_packs / injectable.no_bottles))
		self.assertEqual(injectable.drug.stock_amount, (injectable.drug.purchase_amount * injectable.no_packs * injectable.no_bottles))
		sale_amount = random.randint(1, injectable.drug.purchase_amount)
		injectable.sell(sale_amount, units=drug.units)
		self.assertEqual(injectable.drug.stock_amount, (injectable.drug.purchase_amount - sale_amount) * injectable.no_packs * injectable.no_bottles)
  
		update_amount = random.randint(1, injectable.drug.purchase_amount)
		price=random.randint(1, int(drug.price))
		old_amount = injectable.drug.stock_amount
		injectable.update_stock(update_amount, units=drug.units, price=price)
		self.assertEqual(injectable.drug.price, price / update_amount / injectable.no_packs / injectable.no_bottles)
		self.assertEqual(injectable.drug.stock_amount, old_amount + (update_amount * injectable.no_packs * injectable.no_bottles))





# view drugs

# search drugs