import { shallowMount } from '@vue/test-utils'
import DropdownBase from '../../src/components/SurveyBuilder/DropdownBase'

describe('Dropdown Base test', () => {
  // Create a shallow mount of the dropdownBase vue file
  const wrapper1 = shallowMount(DropdownBase, {
    propsData: {
      options: ['Option 1', 'Option 2', 'Option 3'],
      currentType: null,
    },
    mocks: {
      $t: () => {},
    },
  })

  it('selected data null options test ', () => {
    // Test that the selected value is the first option when currentType is null
    expect(wrapper1.vm.$data.selected).toBe('Option 1')
  })

  it('handleSelection function test', () => {
    // Call the handleSelection function
    wrapper1.vm.handleSelection('Option 3', 1)

    console.log(wrapper1.emitted())

    // Test that the selected option is emitted
    expect(wrapper1.emitted().input[0][0].options).toEqual('Option 3')

    // Test that the selected value is updated
    expect(wrapper1.vm.$data.selected).toBe('p')

    // Test that the open value is updated
    expect(wrapper1.vm.$data.open).toBe(false)
  })

  // Create a shallow mount of the dropdownBase vue file
  const wrapper2 = shallowMount(DropdownBase, {
    propsData: {
      options: null,
      currentType: null,
    },
  })

  it('selected data all null test ', () => {
    // Test that the selected value is null when both currentType and options are null
    expect(wrapper2.vm.$data.selected).toBe(null)
  })
})
