# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError
import unittest
import sys

class TestHospitalPatient(TransactionCase):
    """Unit tests for Hospital Patient in Odoo 15"""

    def setUp(self):
        """Set up test data before each test"""
        super(TestHospitalPatient, self).setUp()

        # Get the patient model
        self.Patient = self.env['hospital.patient']

        # Get or create a responsible person (partner)
        self.Partner = self.env['res.partner']
        self.responsible = self.Partner.create({
            'name': 'Test Responsible Person',
        })

        # Create a test patient
        self.test_patient = self.Patient.create({
            'name': 'Test Dog',
            'responsible_id': self.responsible.id,
            'gender': 'male',
            'age': 15,
        })
    
    def _log_test_start(self, test_name):
        """Log test start"""
        sys.stdout.write(f"{test_name} ... ")
        sys.stdout.flush()
    
    def _log_test_pass(self):
        """Log test pass"""
        sys.stdout.write("ok\n")
        sys.stdout.flush()

    def test_01_create_patient_with_all_fields(self):
        """Test 1: Create a new patient with all required fields"""
        self._log_test_start("test_01_create_patient_with_all_fields")
        
        patient = self.Patient.create({
            'name': 'Test Cat',
            'responsible_id': self.responsible.id,
            'gender': 'female',
            'age': 3,
        })

        self.assertTrue(patient.id, "Patient should be created successfully")
        self.assertEqual(patient.name, 'Test Cat')
        self.assertEqual(patient.age, 3)
        self.assertEqual(patient.gender, 'female')
        self.assertTrue(patient.reference, "Patient should have a reference number")
        
        self._log_test_pass()

    def test_02_update_patient_age_and_responsible(self):
        """Test 2: Update patient age and responsible person"""
        self._log_test_start("test_02_update_patient_age_and_responsible")
        
        new_responsible = self.Partner.create({
            'name': 'Floyd Steward',
        })

        old_age = self.test_patient.age
        self.test_patient.write({
            'age': 25,
            'responsible_id': new_responsible.id,
        })

        self.assertEqual(self.test_patient.age, 25, "Age should be updated to 25")
        self.assertNotEqual(self.test_patient.age, old_age, "Age should be different from original")
        self.assertEqual(self.test_patient.responsible_id.id, new_responsible.id,
                         "Responsible person should be updated")
        
        self._log_test_pass()

    def test_03_search_patients_by_gender(self):
        """Test 3: Search and count patients by gender"""
        self._log_test_start("test_03_search_patients_by_gender")
        
        self.Patient.create({
            'name': 'Test Bird',
            'responsible_id': self.responsible.id,
            'gender': 'male',
            'age': 1,
        })
        self.Patient.create({
            'name': 'Test Fish',
            'responsible_id': self.responsible.id,
            'gender': 'female',
            'age': 2,
        })

        male_patients = self.Patient.search([('gender', '=', 'male')])
        female_patients = self.Patient.search([('gender', '=', 'female')])

        self.assertTrue(len(male_patients) >= 2, 
                        f"Should find at least 2 male patients, found {len(male_patients)}")
        self.assertTrue(len(female_patients) >= 1, 
                        f"Should find at least 1 female patient, found {len(female_patients)}")
        
        self._log_test_pass()

    def test_04_search_patients_by_age_range(self):
        """Test 4: Search patients within age range"""
        self._log_test_start("test_04_search_patients_by_age_range")
        
        self.Patient.create({
            'name': 'Young Patient',
            'responsible_id': self.responsible.id,
            'gender': 'male',
            'age': 5,
        })
        self.Patient.create({
            'name': 'Old Patient',
            'responsible_id': self.responsible.id,
            'gender': 'female',
            'age': 30,
        })

        patients_in_range = self.Patient.search([
            ('age', '>=', 10),
            ('age', '<=', 25)
        ])

        self.assertTrue(len(patients_in_range) >= 1, 
                        f"Should find patients aged 10-25, found {len(patients_in_range)}")
        for patient in patients_in_range:
            self.assertGreaterEqual(patient.age, 10)
            self.assertLessEqual(patient.age, 25)
        
        self._log_test_pass()

    def test_05_delete_patient_and_verify_removed(self):
        """Test 5: Delete a patient and verify it's removed from database"""
        self._log_test_start("test_05_delete_patient_and_verify_removed")
        
        temp_patient = self.Patient.create({
            'name': 'Temporary Patient',
            'responsible_id': self.responsible.id,
            'gender': 'male',
            'age': 10,
        })

        patient_id = temp_patient.id
        patient_reference = temp_patient.reference

        count_before = self.Patient.search_count([])

        temp_patient.unlink()

        count_after = self.Patient.search_count([])

        self.assertEqual(count_after, count_before - 1,
                         "Patient count should decrease by 1 after deletion")

        deleted_patient = self.Patient.search([('id', '=', patient_id)])
        self.assertFalse(deleted_patient, f"Patient {patient_reference} should not exist after deletion")
        
        self._log_test_pass()

    def test_06_intentional_failure(self):
        """Test 6: This test will intentionally fail to verify error logging"""
        self._log_test_start("test_06_intentional_failure")
        
        patient = self.Patient.create({
            'name': 'Test Patient',
            'responsible_id': self.responsible.id,
            'age': 25,
            'gender': 'male',
        })
        
        # This assertion will fail on purpose
        self.assertEqual(patient.age, 99, "Expected age to be 99, but it was 25")
        
        self._log_test_pass()  # This won't be reached if test fails