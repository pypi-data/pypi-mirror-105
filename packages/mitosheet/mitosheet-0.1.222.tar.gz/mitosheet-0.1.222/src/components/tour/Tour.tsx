// Copyright (c) Mito

import React, { useEffect, useState } from 'react';

// Import css
import "../../../css/tour.css"
import { MitoAPI } from '../../api';
import { SheetJSON } from '../../widget';
import XIcon from '../icons/XIcon';
import { TourName, TourPopupLocation, tours, TourStep } from './Tours';


const locationToClassNamesMapping: Record<TourPopupLocation, string> = {
    [TourPopupLocation.BOTTOM_LEFT]: 'tour-container tour-container-bottom-left',
    [TourPopupLocation.BOTTOM_RIGHT]: 'tour-container tour-container-bottom-right',
    [TourPopupLocation.TOP_LEFT]: 'tour-container tour-container-top-left',
    [TourPopupLocation.TOP_RIGHT]: 'tour-container tour-container-top-right',
}

const Tour = (props: {
    mitoAPI: MitoAPI;
    sheetJSON: SheetJSON;
    // TODO: When we make the buttons into components, give them each a highlight props and combine the following two functions
    setHighlightPivotTableButton: (highlight: boolean) => void;
    setHighlightAddColButton: (highlight: boolean) => void; 
    tourNames: TourName[];
}): JSX.Element => {
    const [stepNumber, setStepNumber] = useState<number>(0)
    const [skippedTour, setSkippedTour] = useState<boolean>(false)

    // Construct full list of steps to show by appending the steps of each tour
    // we want to display together. 
    const steps: TourStep[] = []
    props.tourNames.forEach((tourName: TourName) => {
        steps.push(...tours[tourName])
    });

    // Log the beginning of the tour. Because the useEffect has [] as
    // its second param, it only runs once. 
    useEffect(() => {
        void props.mitoAPI.sendLogMessage(
            'begin_tour',
            {
                'tour_names': props.tourNames,
                'total_number_of_tour_steps': steps.length
            }
        )
    }, []);

    /* 
        Each tour is able to register actions that occur at the beginning of specific steps.
        The useEffect is fired each time the stepNumber changes.
    */ 
    useEffect(() => {
        if (steps[stepNumber].tourName === TourName.PIVOT && steps[stepNumber].stepNumber === 1) {
            props.setHighlightPivotTableButton(true)
        } else if (steps[stepNumber].tourName === TourName.COLUMN_FORMULAS && steps[stepNumber].stepNumber === 1) {
            props.setHighlightAddColButton(true)
        } else {
            props.setHighlightPivotTableButton(false)
            props.setHighlightAddColButton(false)
        }
    }, [stepNumber])

    // Go to stepNumber if it exists, otherwise close the tour
    const goToStep = (newStepNumber: number) => {
        if (newStepNumber <= steps.length - 1) {
            // Log switching steps
            void props.mitoAPI.sendLogMessage(
                'switched_tour_step',
                {
                    'old_tour_name': steps[stepNumber].tourName,
                    'old_tour_step': stepNumber,
                    'new_tour_name': steps[newStepNumber].tourName,
                    'new_tour_step': newStepNumber,
                    'tour_names': props.tourNames,
                    'total_number_of_tour_steps': steps.length
                }
            )

            // Update the step number
            setStepNumber(newStepNumber)
        } else {
            void closeTour();
        }
    }

    // Called if you close the tour before you are on the final step
    const closeTourEarly = async (): Promise<void> => {
        void props.mitoAPI.sendLogMessage(
            'closed_tour_early', 
            {
                'tour_names': props.tourNames,
                'tour_name': steps[stepNumber].tourName,
                'relative_tour_step_number': steps[stepNumber].stepNumber, // Log the step number within the tourName so we can identify bad steps
                'absolute_tour_step_number': stepNumber, // Log the total step number so we can see how far users get
                'total_number_of_tour_steps': steps.length // Log the length of the entire tour if they had taken it all
            }
        )

        // Mark that the user skipped the tour so we don't log a finished_tour event
        setSkippedTour(true)

        // Display the final tutorial step
        setStepNumber(steps.length - 1)
    }

    // Called if you close the tour on the final step
    const closeTour = async (): Promise<void> => {
        // Log finishing the tour, if you didn't skip to the final step
        if (!skippedTour) {
            void props.mitoAPI.sendLogMessage(
                'finished_tour', 
                {
                    'tour_names': props.tourNames,
                    'total_number_of_tour_steps': steps.length
                }
            )
        }
        
        // Make sure that the pivot & Add Col button is not stuck in pulsing mode. 
        props.setHighlightPivotTableButton(false)
        props.setHighlightAddColButton(false)

        // Send the closeTour message to the backend. We still record each tour individually
        // so we can later add new tours to display to users
        await props.mitoAPI.sendCloseTour(props.tourNames);
    }

    /* 
        Retrieve the finalStepText, which is the text displayed in the body of the tour popup.
        Although not enforced by the type system, a tour step should either have a defined stepText of stepTextFunction.
    */ 
    const stepText = steps[stepNumber].stepText;
    const stepTextFunction = steps[stepNumber].stepTextFunction;
    const finalStepText = stepText || (stepTextFunction && stepTextFunction(props.sheetJSON.columns[0]));

    // If we're at a valid step number
    return (
        <div className={'tour-container ' + locationToClassNamesMapping[steps[stepNumber].location]} key={stepNumber}>
            <div className='tour-header-container' style={{backgroundColor: steps[stepNumber].stepHeaderBackgroundColor}}>
                {steps[stepNumber].stepHeader}
                <div className='tour-header-close-button' onClick={async () => {
                    if (stepNumber >= steps.length - 1) {
                        await closeTour();
                    } else {
                        await closeTourEarly();
                    }
                }}>
                    <XIcon/>
                </div>
            </div>
            <div className='tour-step-text-container'>
                {finalStepText}
            </div>
            <div className='tour-button-container'>
                {steps[stepNumber].displayBackButton && 
                    <div className='tour-close-button' onClick={() => goToStep(stepNumber - 1)}>
                        Back
                    </div>
                }
                <div className='tour-continue-button' onClick={() => goToStep(stepNumber + 1)}>
                    {steps[stepNumber].advanceButtonText}
                </div>
            </div>
            <div className='tour-progress-bar-container'>
                <p className='tour-progress-bar-text'>
                    {stepNumber + 1}/{steps.length}
                </p>
            </div>
        </div>
    )
}

export default Tour
