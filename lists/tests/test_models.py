from django.core.exceptions import ValidationError
from django.test import TestCase
from lists.models import Item, List


class ItemModelsTest(TestCase):
    
    #OLD - commented out but preserving for reference
    #The two tests below (test_default_text and 
    #test_item_is_related_to_list) test the same functionality
    #
    #def test_saving_and_retrieving_items(self):
    #    newlist = List()
    #    newlist.save()

    #    first_item = Item()
    #    first_item.text = 'The first (ever) list item'
    #    first_item.list = newlist
    #    first_item.save()

    #    second_item = Item()
    #    second_item.text = 'Item the second'
    #    second_item.list = newlist
    #    second_item.save()

    #    saved_list = List.objects.first()
    #    self.assertEqual(saved_list, newlist)

    #    saved_items = Item.objects.all()
    #    self.assertEqual(saved_items.count(), 2)

    #    first_saved_item = saved_items[0]
    #    second_saved_item = saved_items[1]
    #    self.assertEqual(first_saved_item.text, 'The first (ever) list item')
    #    self.assertEqual(first_saved_item.list, newlist)
    #    self.assertEqual(second_saved_item.text, 'Item the second')
    #    self.assertEqual(second_saved_item.list, newlist)

    def test_default_text(self):
        item = Item()
        self.assertEqual(item.text, '')

    def test_item_is_related_to_list(self):
        newlist = List.objects.create()
        item = Item()
        item.list = newlist
        item.save()
        self.assertIn(item, newlist.item_set.all())

    def test_only_saves_items_when_necessary(self):
        self.client.get('/')
        self.assertEqual(Item.objects.count(), 0)

    def test_cannot_save_empty_list_items(self):
        newlist = List.objects.create()
        item = Item(list=newlist, text='')
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()
    
    def test_duplicate_items_are_invalid(self):
        newlist = List.objects.create()
        Item.objects.create(list=newlist, text='test')
        with self.assertRaises(ValidationError):
            item = Item(list=newlist, text='test')
            item.full_clean()

    def test_can_save_same_item_to_different_lists(self):
        list1 = List.objects.create()
        list2 = List.objects.create()
        Item.objects.create(list=list1, text='test')
        item = Item(list=list2, text='test')
        item.full_clean() # No error should occur

    def test_list_ordering(self):
        list1 = List.objects.create()
        item1 = Item.objects.create(list=list1, text='i1')
        item2 = Item.objects.create(list=list1, text='item 2')
        item3 = Item.objects.create(list=list1, text='3')
        self.assertEqual(
            list(Item.objects.all()),
            [item1, item2, item3]
        )

    def test_string_representation(self):
        item = Item(text='some text')
        self.assertEqual(str(item), 'some text')

class ListModelTest(TestCase):

    def test_get_absolute_url(self):
        newlist = List.objects.create()
        self.assertEqual(newlist.get_absolute_url(), f'/lists/{newlist.id}/')

