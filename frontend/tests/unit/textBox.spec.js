import { shallowMount } from '@vue/test-utils'
import TextBox from '../../src/components/SurveyBuilder/TextBox'

describe('Text Box tests', () => {
  it('input test', () => {
    // Create a shallow mount of the TextBox vue file
    const wrapper = shallowMount(TextBox, {
      propsData: {
        placeholder: 'Fake name',
        value: 'Fake value',
        styleClass: 'cool',
      },
      mocks: {
        $t: () => {},
      },
    })

    wrapper.vm.input()

    expect(wrapper.emitted().input[0]).toEqual(['Fake value'])

    expect(wrapper.vm.$data.query).toEqual('Fake value')
  })
})
