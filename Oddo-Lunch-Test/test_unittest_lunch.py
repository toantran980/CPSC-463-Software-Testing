from odoo.tests import common, tagged
from odoo.exceptions import ValidationError
from datetime import datetime
import logging

_logger = logging.getLogger(__name__)

##### A. UNITTEST SUITE #####
@tagged('post_install', '-at_install', 'my_custom_lunch_tests')  # Use Custom tag!
class TestLunchModule(common.TransactionCase):
    """
    Custom Unittest Suite for Lunch Module
    Uses custom tag 'my_custom_lunch_tests' to run separately 3 main test cases
    
    ### CHANGE TO YOUR OWN COMMAND ###
    Sample Run with: python3.9 odoo/odoo-bin \
                -c /etc/odoo15.conf \
                -d odoo15-database \
                --test-enable \
                --test-tags=my_custom_lunch_tests \
                -u lunch \
                --stop-after-init \
                --log-level=test
    """
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.partner = cls.env['res.partner'].create({
            'name': 'Pizza Restaurant Partner',
            'phone': '+1234567890',
        })
        cls.supplier = cls.env['lunch.supplier'].create({
            'name': 'Pizza Restaurant',
            'phone': '+1234567890',
            'partner_id': cls.partner.id,
        })

        cls.category = cls.env['lunch.product.category'].create({
            'name': 'Pizza',
        })
        cls.product = cls.env['lunch.product'].create({
            'name': 'Margherita Pizza',
            'category_id': cls.category.id,
            'price': 12.50,
            'supplier_id': cls.supplier.id,
        })
        
        cls.user = cls.env['res.users'].create({
            'name': 'Test Employee',
            'login': 'test@lunch.com',
        })
        
        cls.location = cls.env['lunch.location'].create({
            'name': 'Main Office',
        })
        
        _logger.info("\n" + "="*70)
        _logger.info("TEST DATA SETUP COMPLETED")
        _logger.info("="*70)

    def test_1_create_valid_lunch_order_positive(self):
        """TEST 1 - CREATE VALID LUNCH ORDER (LIKELY PASS)"""
        _logger.info("\n" + "="*70)
        _logger.info("TEST 1/3: CREATE VALID LUNCH ORDER (POSITIVE)")
        _logger.info("="*70)

        order = self.env['lunch.order'].create({
            'user_id': self.user.id,
            'product_id': self.product.id,
            'date': datetime.today(),
            'lunch_location_id': self.location.id,
        })
        self.assertTrue(order, "Order should be created")
        self.assertEqual(order.state, 'new', "State should be 'new'")
        self.assertEqual(order.price, 12.50, "Price should be 12.50")

        _logger.info(f"Order ID: {order.id}")
        _logger.info(f"Product: {order.product_id.name}")
        _logger.info(f"Price: ${order.price}")
        _logger.info(f"State: {order.state}")
        _logger.info("TEST 1 PASSED")
        _logger.info("="*70)

    def test_2_intentional_failure_negative(self):
        """TEST 2 - INCORRECT PRICE VALUE (INTENTIONAL FAIL)"""
        _logger.info("\n" + "="*70)
        _logger.info("TEST 2/3: INTENTIONAL FAILURE (WRONG PRICE)")
        _logger.info("="*70)

        order = self.env['lunch.order'].create({
            'user_id': self.user.id,
            'product_id': self.product.id,
            'date': datetime.today(),
            'lunch_location_id': self.location.id,
        })

        _logger.info(f"Actual price: ${order.price}")
        _logger.info(f"Expected price (wrong): $99.99")
        _logger.info("THIS ASSERTION WILL FAIL INTENTIONALLY")

        # This will fail b/c 12.50 != 99.99
        self.assertEqual(order.price, 99.99, 
                        "INTENTIONAL FAIL: Expected 99.99 but got 12.50")
        _logger.info("="*70)

    def test_3_order_state_transitions(self):
        """TEST 3 - ORDER STATE TRANSITIONS (LIKELY PASS)"""
        _logger.info("\n" + "="*70)
        _logger.info("TEST 3/3: ORDER STATE TRANSITIONS")
        _logger.info("="*70)

        order = self.env['lunch.order'].create({
            'user_id': self.user.id,
            'product_id': self.product.id,
            'date': datetime.today(),
            'lunch_location_id': self.location.id,
        })

        _logger.info(f"Initial state: {order.state}")
        self.assertEqual(order.state, 'new', "Initial state should be 'new'")

        order.action_confirm()
        _logger.info(f"After confirm: {order.state}")
        self.assertEqual(order.state, 'confirmed', "Should be 'confirmed'")
        
        order.action_cancel()
        _logger.info(f"After cancel: {order.state}")
        self.assertEqual(order.state, 'cancelled', "Should be 'cancelled'")

        _logger.info("All transitions successful: new → confirmed → cancelled")
        _logger.info("TEST 3 PASSED")
        _logger.info("="*70)