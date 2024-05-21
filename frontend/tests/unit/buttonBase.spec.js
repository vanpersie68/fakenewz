import { shallowMount } from '@vue/test-utils'
import ButtonBase from '../../src/components/SurveyBuilder/ButtonBase'

describe('Button Base test', () => {
  // Inspect the raw component options
  // it('has data', () => {
  //   expect(typeof BuilderBlock.data).toBe('function')
  // })

  //Create a shallow mount of the buttonBase vue file
  const wrapper = shallowMount(ButtonBase, {
    propsData: {
      title: 'blocky',
    },
    mocks: {
      $t: () => {},
    },
  })

  //create a mock data object
  const mock_data = jest.fn()

  it('buttonPress function emit test', () => {
    //call the buttonUnfocus function
    wrapper.vm.buttonPress(mock_data)

    //console.log(wrapper.emitted())

    //test that the right object is returned and it has the mock data
    expect(wrapper.emitted().buttonPress[0]).toEqual([mock_data])
  })

  it('buttonUnfocus function emit test', () => {
    //call the buttonUnfocus function
    wrapper.vm.buttonUnfocus()

    //console.log(wrapper.emitted())

    //test that the right object is returned and it is empty
    expect(wrapper.emitted().buttonUnfocus[0]).toEqual([])
  })

  it('mousedown function emit test', () => {
    //call the buttonUnfocus function
    wrapper.vm.mousedown()

    //console.log(wrapper.emitted())

    //test that the right object is returned and it is empty
    expect(wrapper.emitted().mousedown[0]).toEqual([])
  })
})
