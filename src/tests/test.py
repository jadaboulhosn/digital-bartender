import sys
sys.path.insert(0, './')

import logging
import unittest

from backend.bar import Entity, Type, Beverage, Step, Recipe
from backend.barista import Types, Beverages, Recipes
from hal.system import System
from shared.database import Database

class TestEntity(unittest.TestCase):
    def runTest(self):
        # Test different Entities for inequality.
        a = Entity()
        a.one = "alpha"
        a.two = 10
        b = Entity()
        a.one = "bravo"
        a.two = 20
        self.assertNotEqual(a, b, "Different Entities had same IDs!")
        
        # Test identical Entities for equality.
        a = Entity()
        a.one = "alpha"
        a.two = 10
        b = Entity()
        b.one = "alpha"
        b.two = 10
        self.assertEqual(a, b, "Same Entities had different IDs!")

class TestType(unittest.TestCase):
    def runTest(self):
        # Test different Types for inequality.
        a = Type("Vodka")
        b = Type("Tequila")
        self.assertNotEqual(a, b, "Different Types were equal!")

        # Test same Types for equality.
        a = Type("Vodka")
        b = Type("Vodka")
        self.assertEqual(a, b, "Same Types were not equal!")

class TestBeverage(unittest.TestCase):
    def runTest(self):
        # Test different name and Type Beverages for inequality.
        type_a = Type("Vodka")
        a = Beverage("Tito's", type_a)
        type_b = Type("Tequila")
        b = Beverage("Jose Cuervo", type_b)
        self.assertNotEqual(a, b, "Different Beverages were equal!")

        # Test different name and same Type Beverages for inequality.
        type_a = Type("Vodka")
        a = Beverage("Tito's", type_a)
        b = Beverage("Jose Cuervo", type_a)
        self.assertNotEqual(a, b, "Different beverages with same Type were equal!")

        # Test same name and different Type beverages for inequality.
        name = "Tito's"
        type_a = Type("Vodka")
        type_b = Type("Tequila")
        a = Beverage(name, type_a)
        b = Beverage(name, type_b)
        self.assertNotEqual(a, b, "Same name Beverages with different Types were equal!")

        # Test identical Beverages for equality.
        name_a = "Tito's"
        name_b = "Tito's"
        type_a = Type("Vodka")
        type_b = Type("Vodka")
        a = Beverage(name_a, type_a)
        b = Beverage(name_b, type_b)
        self.assertEqual(a, b, "Identical Beverages were not equal!")

class TestStep(unittest.TestCase):
    def runTest(self):
        # Test different Steps for inequality.
        bev_a = Beverage("Tito's", Type("Vodka"))
        bev_b = Beverage("Jose Cuervo", Type("Tequila"))
        step_a = Step(bev_a, 100)
        step_b = Step(bev_b, 200)
        self.assertNotEqual(step_a, step_b, "Different Steps were equal!")

        # Test Steps with same Beverage but different volumes for inequality.
        bev_a = Beverage("Tito's", Type("Vodka"))
        step_a = Step(bev_a, 100)
        step_b = Step(bev_a, 200)
        self.assertNotEqual(step_a, step_b, "Steps with same Beverage but different volumes were equal!")

        # Test Steps with different Beverage but same volume for inequality.
        bev_a = Beverage("Tito's", Type("Vodka"))
        bev_b = Beverage("Jose Cuervo", Type("Tequila"))
        step_a = Step(bev_a, 100)
        step_b = Step(bev_b, 100)
        self.assertNotEqual(step_a, step_b, "Steps with different Beverage but same volume were equal!")

        # Test identical Steps for equality.
        bev_a = Beverage("Tito's", Type("Vodka"))
        bev_b = Beverage("Tito's", Type("Vodka"))
        step_a = Step(bev_a, 100)
        step_b = Step(bev_b, 100)
        self.assertEqual(step_a, step_b, "Identical Steps were not equal!")
        
class TestRecipe(unittest.TestCase):
    def runTest(self):
        # Test different Recipes for inequality.
        rec_a = Recipe("Whiskey Neat")
        rec_a.append(Step(Beverage("Johnny Walker", "Whiskey"), 100))
        rec_b = Recipe("Vodka OJ")
        rec_b.append(Step(Beverage("Smirnoff", "Vodka"), 50))
        rec_b.append(Step(Beverage("Orange Juice", "Mixer"), 150))
        self.assertNotEqual(rec_a, rec_b, "Different Recipes were equal!")

        # Test same Recipes for equality.
        rec_a = Recipe("Whiskey Neat")
        rec_a.append(Step(Beverage("Smirnoff", "Vodka"), 50))
        rec_a.append(Step(Beverage("Orange Juice", "Mixer"), 150))
        rec_b = Recipe("Vodka OJ")
        rec_b.append(Step(Beverage("Smirnoff", "Vodka"), 50))
        rec_b.append(Step(Beverage("Orange Juice", "Mixer"), 150))
        self.assertNotEqual(rec_a, rec_b, "Identical Recipes were not equal!")

class TestTypes(unittest.TestCase):
    def runTest(self):
        # Capture Singletons and clear.
        typ = Types.instance()
        typ.clear()
        bev = Beverages.instance()
        bev.clear()
        rec = Recipes.instance()
        rec.clear()

        # Test contains() method.
        typ.append(Type("Vodka"))
        self.assertTrue(typ.contains(Type("Vodka")), "Contained Type was not found in Types!")
        self.assertFalse(typ.contains(Type("Gin")), "Fictitious Type was found in Types!")
        typ.clear()

        # Test remove() method.
        typ.append(Type("Vodka"))
        self.assertTrue(typ.remove(Type("Vodka")), "Unable to remove Type from Types!")
        self.assertFalse(typ.remove(Type("Gin")), "Removed a Fictitious Type from Types!")
        typ.clear()

        # Test remove() method destroying downstream references.
        # Add Types.
        type_a = Type("Vodka")
        type_b = Type("Tequila")
        type_c = Type("Mixer")
        typ.append(type_a)
        typ.append(type_b)
        typ.append(type_c)

        # Add Beverages.
        bev_a = Beverage("Smirnoff", type_a)
        bev_b = Beverage("1800s", type_b)
        bev_c = Beverage("Orange Juice", type_c)
        bev_d = Beverage("Squirt", type_c)
        bev.append(bev_a)
        bev.append(bev_b)
        bev.append(bev_c)
        bev.append(bev_d)
        
        # Add Recipes.
        rec_a = Recipe("Vodka OJ")
        rec_a.append(Step(bev_a, 50))
        rec_a.append(Step(bev_c, 200))
        rec_b = Recipe("Tequila Squirt")
        rec_b.append(Step(bev_b, 50))
        rec_b.append(Step(bev_d, 200))
        rec.append(rec_a)
        rec.append(rec_b)

        # Test 1: Remove a base Type.
        self.assertTrue(typ.remove(type_a), "Failed to remove a Type with downstream references.")
        self.assertEqual(len(typ), 2, "More Types remaining than expected!")

        # Test 2: Check if downstream Beverage has been destroyed.
        self.assertFalse(bev.contains(bev_a), "Destroyed Type left Beverage intact!")
        self.assertEqual(len(bev), 3, "More Beverages remaining than expected!")

        # Test 3: Check if downstream recipe has been destroyed.
        self.assertFalse(rec.contains(rec_a), "Destroyed Type left Recipe intact!")
        self.assertEqual(len(rec), 1, "More Recipes remaining than expected!")

        typ.clear()
        bev.clear()
        rec.clear()

class TestBeverages(unittest.TestCase):
    def runTest(self):
        # Capture Singletons and clear.
        typ = Types.instance()
        typ.clear()
        bev = Beverages.instance()
        bev.clear()
        rec = Recipes.instance()
        rec.clear()

        # Test contains() method.
        bev.append(Beverage("Smirnoff", Type("Vodka")))
        self.assertTrue(bev.contains(Beverage("Smirnoff", Type("Vodka"))), "Contained Beverage was not found in Beverages!")
        self.assertFalse(bev.contains(Beverage("Seagrams", Type("Gin"))), "Fictitious Beverage was found in Beverages!")
        bev.clear()

        # Test remove() method.
        bev.append(Beverage("Smirnoff", Type("Vodka")))
        self.assertTrue(bev.remove(Beverage("Smirnoff", Type("Vodka"))), "Contained Beverage was not found in Beverages!")
        self.assertFalse(bev.remove(Beverage("Seagrams", Type("Gin"))), "Fictitious Beverage was found in Beverages!")
        bev.clear()

        # Test remove() method destroying downstream references.
        # Add Types.
        type_a = Type("Vodka")
        type_b = Type("Tequila")
        type_c = Type("Mixer")
        typ.append(type_a)
        typ.append(type_b)
        typ.append(type_c)

        # Add Beverages.
        bev_a = Beverage("Smirnoff", type_a)
        bev_b = Beverage("1800s", type_b)
        bev_c = Beverage("Orange Juice", type_c)
        bev_d = Beverage("Squirt", type_c)
        bev.append(bev_a)
        bev.append(bev_b)
        bev.append(bev_c)
        bev.append(bev_d)
        
        # Add Recipes.
        rec_a = Recipe("Vodka OJ")
        rec_a.append(Step(bev_a, 50))
        rec_a.append(Step(bev_c, 200))
        rec_b = Recipe("Tequila Squirt")
        rec_b.append(Step(bev_b, 50))
        rec_b.append(Step(bev_d, 200))
        rec.append(rec_a)
        rec.append(rec_b)

        # Test 1: Remove a base Beverage.
        self.assertTrue(bev.remove(bev_a), "Failed to remove a Type with downstream references.")
        self.assertEqual(len(bev), 3, "More Types remaining than expected!")

        # Test 3: Check if downstream recipe has been destroyed.
        self.assertFalse(rec.contains(rec_a), "Destroyed Type left Recipe intact!")
        self.assertEqual(len(rec), 1, "More Recipes remaining than expected!")

        typ.clear()
        bev.clear()
        rec.clear()

class TestRecipes(unittest.TestCase):
    def runTest(self):
        # Capture Singletons and clear.
        typ = Types.instance()
        typ.clear()
        bev = Beverages.instance()
        bev.clear()
        rec = Recipes.instance()
        rec.clear()

        # Test remove() method destroying downstream references.
        # Add Types.
        type_a = Type("Vodka")
        type_b = Type("Tequila")
        type_c = Type("Mixer")
        typ.append(type_a)
        typ.append(type_b)
        typ.append(type_c)

        # Add Beverages.
        bev_a = Beverage("Smirnoff", type_a)
        bev_b = Beverage("1800s", type_b)
        bev_c = Beverage("Orange Juice", type_c)
        bev_d = Beverage("Squirt", type_c)
        bev.append(bev_a)
        bev.append(bev_b)
        bev.append(bev_c)
        bev.append(bev_d)
        
        # Add Recipes.
        rec_a = Recipe("Vodka OJ")
        rec_a.append(Step(bev_a, 50))
        rec_a.append(Step(bev_c, 200))
        rec_b = Recipe("Tequila Squirt")
        rec_b.append(Step(bev_b, 50))
        rec_b.append(Step(bev_d, 200))
        rec.append(rec_a)
        rec.append(rec_b)

        # Test 1: Remove a base Type.
        self.assertTrue(rec.remove(rec_a), "Failed to remove a Recipe!")
        self.assertEqual(len(rec), 1, "More Recipes remaining than expected!")

        typ.clear()
        bev.clear()
        rec.clear()

class TestSystem(unittest.TestCase):
    def runTest(self):
        dev = System.instance()
        dev.clear()

        # Create fake valid Pump.
        p_one = dev.attach("Test Pump 1", 33, 31)
        self.assertTrue(p_one.is_valid(), "Valid pump was marked invalid!")

        # Test functions.
        self.assertFalse(p_one.deactivate(), "Inactive pump was deactivated!")
        self.assertTrue(p_one.activate(), "Unable to activate a valid pump!")
        self.assertTrue(p_one.is_active(), "Pump was not active despite being activated!")
        self.assertTrue(p_one.deactivate(), "Unable to deactivate a valid pump!")

        # Create fake invalid Pump.
        p_two = dev.attach("Test Pump 2", 1, 2)
        self.assertFalse(p_two.is_valid(), "Invalid pump was marked valid!")

        # Test functions.
        self.assertFalse(p_two.activate(), "Invalid pump was activated!")
        self.assertFalse(p_two.is_active(), "Invalid pump was active!")
        self.assertFalse(p_two.deactivate(), "Invalid pump was deactivated!")

        dev.clear()

class TestDatabase(unittest.TestCase):
    def runTest(self):
        # Capture Singletons and clear.
        typ = Types.instance()
        typ.clear()
        bev = Beverages.instance()
        bev.clear()
        rec = Recipes.instance()
        rec.clear()
        dev = System.instance()
        dev.clear()

        # Add Types.
        type_a = Type("Vodka")
        type_b = Type("Tequila")
        type_c = Type("Mixer")
        typ.append(type_a)
        typ.append(type_b)
        typ.append(type_c)

        # Add Beverages.
        bev_a = Beverage("Smirnoff", type_a)
        bev_b = Beverage("1800s", type_b)
        bev_c = Beverage("Orange Juice", type_c)
        bev_d = Beverage("Squirt", type_c)
        bev.append(bev_a)
        bev.append(bev_b)
        bev.append(bev_c)
        bev.append(bev_d)
        
        # Add Recipes.
        rec_a = Recipe("Vodka OJ")
        rec_a.append(Step(bev_a, 50))
        rec_a.append(Step(bev_c, 200))
        rec_b = Recipe("Tequila Squirt")
        rec_b.append(Step(bev_b, 50))
        rec_b.append(Step(bev_d, 200))
        rec.append(rec_a)
        rec.append(rec_b)

        # Create a Database.
        database = Database("../data/test/")

        # Create fake valid Pump.
        p_one = dev.attach("Test Pump 1", 33, 31)
        self.assertTrue(p_one.is_valid(), "Valid pump was marked invalid!")

        # Create fake invalid Pump.
        p_two = dev.attach("Test Pump 2", 1, 2)
        self.assertFalse(p_two.is_valid(), "Invalid pump was marked valid!")

        # Collect Serialization IDs.
        prev_ids = []
        for t in typ:
            prev_ids.append(hash(t))

        for b in bev:
            prev_ids.append(hash(b))
        
        for r in rec:
            prev_ids.append(hash(r))

        # Test saving the database.
        self.assertTrue(database.save(), "Failed to save Database!")

        # Test loading the database.
        self.assertTrue(database.load(), "Failed to load Database!")

        # Collect new Serialization IDs.
        ids = []
        for t in typ:
            ids.append(hash(t))

        for b in bev:
            ids.append(hash(b))
        
        for r in rec:
            ids.append(hash(r))

        # Test number of objects.
        self.assertEqual(len(prev_ids), len(ids), "Database returned different number of objects than saved!")

        # Test ID equality.
        for id in ids:
            self.assertTrue(id in prev_ids, "An ID mismatch occured after reserialization!")

        # Test pump count.
        self.assertTrue(len(dev) == 2, "Unexpected number of pumps returned.")

        database.destroy()
        typ.clear()
        bev.clear()
        rec.clear()
        dev.clear()

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.INFO)
unittest.main()