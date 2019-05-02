from django.core.exceptions import ValidationError
from django.test import TestCase
from lists.models import Item, List


class ListAndItemModelsTest(TestCase):
    
    def test_saving_and_retrieving_items(self):
        newlist = List()
        newlist.save()

        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.list = newlist
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.list = newlist
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, newlist)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(first_saved_item.list, newlist)
        self.assertEqual(second_saved_item.text, 'Item the second')
        self.assertEqual(second_saved_item.list, newlist)

    def test_only_saves_items_when_necessary(self):
        self.client.get('/')
        self.assertEqual(Item.objects.count(), 0)

    def test_cannot_save_empty_list_items(self):
        newlist = List.objects.create()
        item = Item(list=newlist, text='')
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()
    
    def test_get_absolute_url(self):
        newlist = List.objects.create()
        self.assertEqual(newlist.get_absolute_url(), f'/lists/{newlist.id}/')
