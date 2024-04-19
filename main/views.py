from django.conf import settings
from django.shortcuts import render, HttpResponse
import os
import random


def home(response):
    return render(response, "main/home.html", {})


def about(response):
    return render(response, "main/about.html", {})


def pick_random_image(directory1, directory2):
    # Use relative paths from the static directory.
    directory1_path = os.path.join(settings.STATIC_ROOT, directory1)
    directory2_path = os.path.join(settings.STATIC_ROOT, directory2)

    # Pick random images as previously
    image1 = random.choice(os.listdir(directory1_path))
    image2 = random.choice(os.listdir(directory2_path))

    return image1, image2


def show_image(request):
    directory1 = "fakeTweet"  # Assumes we're already in the static directory.
    directory2 = "realTweet"  # Same as above.
    image1, image2 = pick_random_image(directory1, directory2)
    chosen_image = random.choice([image1, image2])
    image_path = os.path.join(directory1 if chosen_image == image1 else directory2, chosen_image)
    # Store the result in session
    request.session['chosen_image'] = chosen_image
    # Pass image_path to the template for display.
    return render(request, 'main/game.html', {'image_path': image_path})


def submit_guess(request):
    chosen_image = request.session.get('chosen_image')

    if chosen_image is None:
        return HttpResponse("No image chosen yet.")

    # Check if chosen_image is from real tweet folder
    is_real = 'realTweet' in chosen_image

    if request.method == 'POST':
        user_choice = request.POST.get('guess')

        if (user_choice == 'real' and is_real) or (user_choice == 'fake' and not is_real):
            response = "You guessed correctly!"
        elif (user_choice == 'real' and not is_real) or (user_choice == 'fake' and is_real):
            response = "Sorry, your guess was incorrect."
        else:
            response = "Invalid input."

        return HttpResponse(response)
    else:
        return HttpResponse("Method not allowed.")
