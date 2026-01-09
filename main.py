import flet as ft
import flet_map as map
import flet_audio as fta


def main(page: ft.Page):
    
    global image_width, image_height, text_size
    def update_layout(e):
        global image_width, image_height, text_size
        if page.width < page.height:
            #Mobile
            image_width = 320
            image_height = 240
            text_size = 25
        else:
            #Desktop
            image_width = 640
            image_height = 480
            text_size = 50


        page.update()

    page.on_resize = update_layout

    update_layout(None)

    
    marker_layer_ref = ft.Ref[map.MarkerLayer]()

    def infos_audio_event(e):
        global audio_state
        if audio_state == 0:
            audio_state = 1
            infos_audio.play()
            infos_audio_button.content=ft.Icon(ft.Icons.PAUSE_CIRCLE_ROUNDED, size=35)
        elif audio_state == 1:
            infos_audio.pause()
            infos_audio_button.content=ft.Icon(ft.Icons.PLAY_CIRCLE_ROUNDED, size=35)
            audio_state = 2
        else:
            infos_audio.resume()
            infos_audio_button.content=ft.Icon(ft.Icons.PAUSE_CIRCLE_ROUNDED, size=35)
            audio_state = 1
        infos_audio_button.update()



    infos_audio = fta.Audio(
        src='https://luan.xyz/files/audio/ambient_c_motion.mp3',
        autoplay=False,
    )
    page.overlay.append(infos_audio)
    page.title = 'Audioguide Berlin'

    global audio_state
    audio_state = 0

    def back_event(e):
        global audio_state
        audio_state = 0
        infos_audio.pause()
        main_map.visible = True
        infos.visible = False
        infos_audio_button.content = ft.Icon(ft.Icons.PLAY_CIRCLE_ROUNDED, size=35)

        page.update()

    infos_back_button = ft.TextButton('Revenir à la carte', on_click=back_event)

    infos_audio_button = ft.TextButton(
        on_click=infos_audio_event,
        content=ft.Icon(ft.Icons.PLAY_CIRCLE_ROUNDED, size=35),
        style=ft.ButtonStyle(
            color="#ffffff",
            bgcolor="#1f5eff",
            shape=ft.CircleBorder(),
            padding=15,
        ))
    infos_audio_restart = ft.TextButton(
        on_click=lambda _: infos_audio.seek(0),
        content=ft.Icon(ft.Icons.RESTART_ALT_ROUNDED, size=35),
        style=ft.ButtonStyle(
            color="#ffffff",
            bgcolor="#1f5eff",
            shape=ft.CircleBorder(),
            padding=15,
        ))

    infos_title = ft.Text('...', size=text_size)

    infos_image = ft.Image(width=image_width, height=image_height)

    infos_column = ft.Column([
        ft.Row([infos_title], alignment=ft.MainAxisAlignment.CENTER),
        ft.Row([infos_image], alignment=ft.MainAxisAlignment.CENTER),
        ft.Row([infos_audio_button, infos_audio_restart], alignment=ft.MainAxisAlignment.CENTER),
        ft.Row([infos_back_button], alignment=ft.MainAxisAlignment.CENTER),

    ], expand=True, alignment=ft.MainAxisAlignment.CENTER)


    infos = ft.Container(infos_column, expand=True, visible=False, alignment=ft.alignment.center)

    def marker_event(title, audio, image):
        global audio_state
        audio_state = 0
        infos_audio.seek(0)
        infos_title.value = title
        infos_audio.src = audio
        infos_audio.update()
        infos_image.src = image
        main_map.visible = False
        infos.visible = True
        page.update()


    def handle_tap(e: map.MapTapEvent):
        print(e.coordinates)
        page.update()

    main_map = map.Map(
            expand=True,
            initial_center=map.MapLatitudeLongitude(52.5172200412667, 13.395079719263894),
            initial_zoom=15,
            interaction_configuration=map.MapInteractionConfiguration(
                flags=map.MapInteractiveFlag.ALL  & ~map.MapInteractiveFlag.ROTATE
            ),
            on_init=lambda e: print(f"Initialized Map"),
            on_tap=handle_tap,
            on_secondary_tap=handle_tap,
            on_long_press=handle_tap,
            # on_event=lambda e: print(e),
            layers=[
                map.TileLayer(
                    url_template="https://tile.openstreetmap.org/{z}/{x}/{y}.png",
                ),
                map.MarkerLayer(
                    ref=marker_layer_ref,
                    markers=[
                    ],
                ),

            ],
        )

    page.add(
        main_map,infos
    )

    markers = [
        map.Marker(
            content=ft.Container(
                ft.Icon(ft.Icons.LOCATION_ON, color=ft.CupertinoColors.DESTRUCTIVE_RED, size=50),
                on_click=lambda _: marker_event(
                    'Brandenburger Tor',
                    'Berlin_Oral_BrandenBürger_Tor.mp3',
                    'brandenburger_tor.jpg'
                )
            ),
            coordinates=map.MapLatitudeLongitude(52.516272046556736, 13.37770125331996),
        ),
        map.Marker(
            content=ft.Container(
                ft.Icon(ft.Icons.LOCATION_ON, color=ft.CupertinoColors.DESTRUCTIVE_RED, size=50),
                on_click=lambda _: marker_event(
                    'Reichstag',
                    'Oral_Berlin_Reichstag.mp3',
                    'reichstag.jpg'
                )
            ),
            coordinates=map.MapLatitudeLongitude(52.518595503550465, 13.376103110139926),
        ),
        map.Marker(
            content=ft.Container(
                ft.Icon(ft.Icons.LOCATION_ON, color=ft.CupertinoColors.DESTRUCTIVE_RED, size=50),
                on_click=lambda _: marker_event(
                    'Checkpoint Charlie',
                    'Yeni_Kayit_8.mp3',
                    'checkpoint_charlie.jpg'
                )
            ),
            coordinates=map.MapLatitudeLongitude(52.506045835499755, 13.39061238001653),
        ),
        map.Marker(
            content=ft.Container(
                ft.Icon(ft.Icons.LOCATION_ON, color=ft.CupertinoColors.DESTRUCTIVE_RED, size=50),
                on_click=lambda _: marker_event(
                    'Gedenkstätte Deutscher Widerstand',
                    'Yeni_Kayit_7.mp3',
                    'german-resistance-memorial-berlin.jpg'
                )
            ),
            coordinates=map.MapLatitudeLongitude(52.50758841506009, 13.362997509894775),
        ),
        map.Marker(
            content=ft.Container(
                ft.Icon(ft.Icons.LOCATION_ON, color=ft.CupertinoColors.DESTRUCTIVE_RED, size=50),
                on_click=lambda _: marker_event(
                    'Gedenkstätte Berlin-Hohenschönhausen',
                    'Yeni_Kayit_6.mp3',
                    'Gedenkstatte.jpg'
                )
            ),
            coordinates=map.MapLatitudeLongitude(52.54170069093194, 13.50134937473682),
        ),
        map.Marker(
            content=ft.Container(
                ft.Icon(ft.Icons.LOCATION_ON, color=ft.CupertinoColors.DESTRUCTIVE_RED, size=50),
                on_click=lambda _: marker_event(
                    'Sachsenhausen',
                    'sachsenhausen.mp3',
                    'sachsenhausen.jpg',

                )
            ),
            coordinates=map.MapLatitudeLongitude(52.76712141099976, 13.262310337506806),
        ),
        map.Marker(
            content=ft.Container(
                ft.Icon(ft.Icons.LOCATION_ON, color=ft.CupertinoColors.DESTRUCTIVE_RED, size=50),
                on_click=lambda _: marker_event(
                    'Berlin Story Bunker',
                    'h_bunker.mp3',
                    'bunker.jpg'
                )
            ),
            coordinates=map.MapLatitudeLongitude(52.502901807796526, 13.380349434064692),
        ),
        map.Marker(
            content=ft.Container(
                ft.Icon(ft.Icons.LOCATION_ON, color=ft.CupertinoColors.DESTRUCTIVE_RED, size=50),
                on_click=lambda _: marker_event(
                    'Das Holocaust-Mahnmal',
                    'holocaust_Mahmal.mp3',
                    'manhmal.jpg'
                )
            ),
            coordinates=map.MapLatitudeLongitude(52.51387042814625, 13.378731404820462),
        ),
    ]

    marker_layer_ref.current.markers = markers

    page.update()



ft.app(main, assets_dir='assets')



