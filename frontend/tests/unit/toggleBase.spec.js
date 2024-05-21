import { shallowMount } from '@vue/test-utils'
import ToggleBase from '../../src/components/SurveyBuilder/ToggleBase.vue'

describe('Toggle Base test', () => {
  it('handleToggle onclick function emit test', () => {
    // Create a shallow mount of the theToolBar vue file
    const wrapper = shallowMount(ToggleBase, {
      propsData: {
        toggled: false,
      },
    })

    // Call the handleToggle function
    wrapper.vm.handleToggle()

    console.log(wrapper.emitted())

    // Test that nothing is emitted
    expect(wrapper.emitted().handleToggle).toEqual([[]])
  })

  it('handleToggle toggleValue computed test', async () => {
    // Create a shallow mount of the theToolBar vue file
    const wrapper = shallowMount(ToggleBase, {
      propsData: {
        toggled: true,
      },
    })

    // Test that the computed property is true when toggled is true
    expect(wrapper.vm.toggleValue).toBe(true)

    // Test that the computed property is false when toggled is false
    await wrapper.setProps({ toggled: false })
    expect(wrapper.vm.toggleValue).toBe(false)

    // Test that the computed property can't be altered
    wrapper.vm.toggleValue = true
    expect(wrapper.vm.toggleValue).toBe(false)
  })
})
