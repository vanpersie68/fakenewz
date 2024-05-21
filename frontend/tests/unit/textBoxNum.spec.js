import { shallowMount } from '@vue/test-utils'
import TextBoxNum from '../../src/components/SurveyBuilder/TextBoxNum'

describe('TextBoxNum test suite', () => {
  it('update test', () => {
    // Create a shallow mount of the TextBox vue file
    const wrapper = shallowMount(TextBoxNum, {
      propsData: {
        placeholder: 'Fake name',
        initialValue: '9',
        value: '10',
      },
      mocks: {
        $t: () => {},
      },
    })

    wrapper.vm.update()

    expect(wrapper.emitted().update[0]).toEqual([10])

    expect(wrapper.vm.$data.query).toEqual('10')
  })

  it('increment test', () => {
    // Create a shallow mount of the TextBox vue file
    const wrapper = shallowMount(TextBoxNum, {
      propsData: {
        placeholder: 'Fake name',
        initialValue: '9',
        value: '10',
      },
      mocks: {
        $t: () => {},
      },
    })

    wrapper.vm.increment()

    expect(wrapper.emitted().increment[0]).toEqual([])

    expect(wrapper.vm.$data.query).toEqual('10')
  })

  it('decrement test', () => {
    // Create a shallow mount of the TextBox vue file
    const wrapper = shallowMount(TextBoxNum, {
      propsData: {
        placeholder: 'Fake name',
        initialValue: '9',
        value: '10',
      },
      mocks: {
        $t: () => {},
      },
    })

    wrapper.vm.decrement()

    expect(wrapper.emitted().decrement[0]).toEqual([])

    expect(wrapper.vm.$data.query).toEqual('10')
  })

  it('set(NewValue) test', () => {
    // Create a shallow mount of the TextBox vue file
    const wrapper = shallowMount(TextBoxNum, {
      propsData: {
        placeholder: 'Fake name',
        initialValue: '9',
        value: '10',
      },
      mocks: {
        $t: () => {},
      },
    })

    wrapper.setData({ compQuery: '15' })

    expect(wrapper.vm.$data.query).toEqual('15')
  })
})
