import store from '../store/SurveyBuilder.js'

export const applyDrag = (block, dragResult) => {
  const { removedIndex, addedIndex, payload } = dragResult
  console.log(dragResult)

  // Payload is the question
  let itemToAdd = payload

  // Have the find the block from which the question came
  let oldBlock

  // The order of the question prior to being dropped.
  // NEED TO FIX THE ORDERING OF THE PREEXISTING BLOCK
  let oldOrder = itemToAdd.order

  let blockList = store.getters['blocks']

  for (let i = 0; i < blockList.length; i++) {
    for (let j = 0; j < blockList[i].questionData.questions.length; j++) {
      if (blockList[i].questionData.questions[j] === itemToAdd) {
        oldBlock = blockList[i]
      }
    }
  }

  if (addedIndex !== null) {
    // If the question was moved and placed within the SAME block
    if (oldBlock === block) {
      // Checks if it was moved to a different order within the block
      if (oldOrder != addedIndex) {
        store.commit('insertQuestionDragDrop', {
          block: block,
          question: itemToAdd,
          order: addedIndex,
          oldBlock: oldBlock,
        })
      }
      // If the question was moved and placed within ANOTHER block
    } else if (!(oldBlock === block)) {
      store.commit('insertQuestionDragDrop', {
        block: block,
        question: itemToAdd,
        order: addedIndex,
        oldBlock: oldBlock,
      })
    }

    // does this delete the question model that preexisting prior to 'placing' a new
    if (!(oldBlock === block)) {
      store.commit('deleteQuestionDragDrop', {
        oldOrder: oldOrder,
        oldBlock: oldBlock,
        question: itemToAdd,
        newBlock: block,
      })
    }
  }
}

export const applyFlowDrag = (orderedFlow, dragResult) => {
  // TODO: Make random sections work for delete and duplicate?

  // If not dragged anywhere => do nothing
  if (dragResult.removedIndex == dragResult.addedIndex) {
    return
  }

  // If dragging a start block:
  // If it is now after or adjacent to it's end block => do nothing
  // If it now overlaps with another randomised section => do nothing
  // Else => startWith = order of next adjacent block's order
  if (dragResult.payload.start) {
    let endIndex = orderedFlow.indexOf(
      orderedFlow.filter(
        (e) => e.start == false && e.startInd == dragResult.payload.startInd
      )[0]
    )
    let endValue = store.getters.randomSections.filter(
      (e) => e.startWith == dragResult.payload.startInd
    )[0].endWith

    // Set to next block order (plus 1 if moving downwards)
    let newValue
    if (dragResult.addedIndex > dragResult.removedIndex) {
      newValue = orderedFlow[dragResult.addedIndex].order + 1
    } else {
      newValue = orderedFlow[dragResult.addedIndex].order
    }
    if (newValue == null) {
      return
    }

    // If the new start is before the old end (and not immediately adjacent)
    if (dragResult.addedIndex < endIndex - 1) {
      // If there are no other ends between it and it's end...
      for (let i = 0; i < store.getters.randomSections.length; i++) {
        if (
          store.getters.randomSections[i].startWith !=
          dragResult.payload.startInd
        ) {
          if (
            (newValue >= store.getters.randomSections[i].startWith &&
              newValue <= store.getters.randomSections[i].endWith) || // Inside the section
            (newValue <= store.getters.randomSections[i].startWith &&
              endValue >= store.getters.randomSections[i].endWith)
          ) {
            // Encapsulating the section
            return
          }
        }
      }

      // If you reach here, then the move is valid, apply changes
      store.commit('updateStartWith', {
        oldStart: dragResult.payload.startInd,
        newStart: newValue,
      })
    }

    // If dragging an end block:
    // If it is now before or adjacent to it's start block => do nothing
    // If it now overlaps with another randomised section => do nothing
    // Else => endWith = order of previous adjacent block's order
  } else if (dragResult.payload.start == false) {
    let startIndex = orderedFlow.indexOf(
      orderedFlow.filter(
        (e) => e.start == true && e.startInd == dragResult.payload.startInd
      )[0]
    )
    let startValue = store.getters.randomSections.filter(
      (e) => e.startWith == dragResult.payload.startInd
    )[0].startWith

    // Set to next block order (plus 1 if moving downwards)
    let newValue
    if (dragResult.addedIndex > dragResult.removedIndex) {
      newValue = orderedFlow[dragResult.addedIndex].order
    } else {
      newValue = orderedFlow[dragResult.addedIndex - 1].order
    }
    if (newValue == null || isNaN(newValue)) {
      return
    }

    // If the new old is after the section's start (and not immediately adjacent)
    if (dragResult.addedIndex > startIndex + 1) {
      // If there are no other starts between it and it's start...
      for (let i = 0; i < store.getters.randomSections.length; i++) {
        if (
          store.getters.randomSections[i].startWith !=
          dragResult.payload.startInd
        ) {
          if (
            (newValue >= store.getters.randomSections[i].startWith &&
              newValue <= store.getters.randomSections[i].endWith) || // Inside the section
            (newValue >= store.getters.randomSections[i].endWith &&
              startValue <= store.getters.randomSections[i].startWith)
          ) {
            // Encapsulating the section
            return
          }
        }
      }

      // If you reach here, then the move is valid, apply changes
      store.commit('updateEndWith', {
        oldStart: dragResult.payload.startInd,
        newEnd: newValue,
      })
    }

    // If dragging a block:
    //TODO: FIX THIS SECTION!
  } else {
    // Find what order the block is being moved to
    let newOrder = orderedFlow[dragResult.addedIndex].order
    console.log('NEW', newOrder)

    if (newOrder == null) {
      // If dragging to replace a start block
      if (orderedFlow[dragResult.addedIndex].start) {
        // If dragging down => Insert inside
        if (dragResult.addedIndex > dragResult.removedIndex) {
          newOrder = orderedFlow[dragResult.addedIndex].startInd - 1

          // If dragging up => Insert outside
        } else {
          newOrder = orderedFlow[dragResult.addedIndex].startInd
        }
        // If dragging to replace an end block
      } else {
        // If dragging down => Insert outside
        if (dragResult.addedIndex > dragResult.removedIndex) {
          newOrder = store.getters.randomSections.filter(
            (e) => e.startWith == orderedFlow[dragResult.addedIndex].startInd
          )[0].endWith
        } else {
          newOrder =
            store.getters.randomSections.filter(
              (e) => e.startWith == orderedFlow[dragResult.addedIndex].startInd
            )[0].endWith + 1
        }
      }
    }
    //     console.log("NULL")

    //     if (orderedFlow[dragResult.addedIndex].start) {
    //         console.log("DRAGGING TO A START")

    //         // If above a start block
    //         newOrder = orderedFlow[dragResult.addedIndex].startInd;

    //         newOrder = orderedFlow[dragResult.addedIndex].startInd;
    //         console.log(newOrder)
    //         // Decrement random section startWith

    //     } else {
    //         console.log("DRAGGING TO AN END")

    //         newOrder = store.getters.randomSections.filter(e => e.startWith == orderedFlow[dragResult.addedIndex].startInd)[0].endWith
    //         // Decrement random section endWith
    //         store.commit('updateEndWith', {
    //             oldStart: orderedFlow[dragResult.addedIndex].startInd,
    //             newEnd: store.getters.randomSections.filter(e => e.startWith == orderedFlow[dragResult.addedIndex].startInd)[0].endWith - 1
    //         })

    //     }
    // }

    let thisBlock =
      store.getters.sortedBlocks[orderedFlow[dragResult.removedIndex].order - 1]

    let newOrderedFlow = orderedFlow
    // If dragging down
    if (dragResult.addedIndex > dragResult.removedIndex) {
      newOrderedFlow.splice(
        dragResult.addedIndex + 1,
        0,
        orderedFlow[dragResult.removedIndex]
      )
      newOrderedFlow.splice(dragResult.removedIndex, 1)

      // If dragging up
    } else {
      newOrderedFlow.splice(
        dragResult.addedIndex,
        0,
        orderedFlow[dragResult.removedIndex]
      )
      newOrderedFlow.splice(dragResult.removedIndex + 1, 1)
    }

    // Adjust random section bounds to match newOrderedFlow
    let order = 0
    for (let i = 0; i < newOrderedFlow.length; i++) {
      if (newOrderedFlow[i].order != null) {
        order++
      } else {
        // If it is a start random section bound...
        let thisSection = store.getters.randomSections.filter(
          (e) => e.startWith == newOrderedFlow[i].startInd
        )[0]
        if (newOrderedFlow[i].start) {
          // Also update the endWith coming to this startInd
          newOrderedFlow.filter(
            (e) => !e.start && e.startInd == newOrderedFlow[i].startInd
          )[0].startInd = order + 1

          store.commit('updateStartWith', {
            oldStart: thisSection.startWith,
            newStart: order + 1,
          })
        } else {
          store.commit('updateEndWith', {
            oldStart: thisSection.startWith,
            newEnd: order,
          })
        }
      }
    }

    // Automatically deletes all random sections of size 0
    for (let i = store.getters.randomSections.length - 1; i > -1; i--) {
      if (
        store.getters.randomSections[i].endWith <
        store.getters.randomSections[i].startWith
      ) {
        store.commit(
          'removeRandomSection',
          store.getters.randomSections[i].startWith
        )
      }
    }

    store.commit('moveBlock', {
      newOrder: newOrder,
      block: thisBlock,
    })
  }
}
