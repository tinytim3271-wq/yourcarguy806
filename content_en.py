"""English content. Each service/area has a stable `key` shared with content_es.py."""
CALL = "(806) 451-3520"
TEXT = "(806) 776-4460"

UI = {
    "lang": "en-US", "og_locale": "en_US", "name": "English", "short": "EN",
    "prefix": "",
    "paths": {"home": "/", "services": "/services/", "area": "/service-area/", "about": "/about/",
              "contact": "/contact/", "terms": "/terms/", "privacy": "/privacy/", "sms": "/sms/"},
    "skip": "Skip to content",
    "topbar_left": "Mobile mechanic &middot; Lubbock County &amp; surrounding towns",
    "call": "Call", "text": "Text", "call_now": "Call Now", "send_text": "Send a Text",
    "nav": ["Services", "Service Area", "About", "Contact"],
    "menu": "Menu", "close": "Close", "home_label": "home",
    "lang_switch_label": "Ver en español", "lang_setting": "Language / Idioma",
    "request_service": "Request Service", "learn_more": "Learn more",
    "crumb_home": "Home",
    "cta_h": "Broke down? We come to you.",
    "cta_p": "Call or text for a quote. Lubbock County and surrounding towns.",
    "footer_about": "Reliable Automotive Services is a mobile mechanic serving Lubbock, Lubbock County, and surrounding West Texas towns. We bring the shop to your driveway.",
    "f_services": "Services", "f_area": "Service Area", "f_company": "Company",
    "all_services": "All services", "all_areas": "All areas", "about": "About",
    "contact_req": "Contact &amp; Request Service", "text_us": "Text us",
    "terms": "Terms of Service", "privacy": "Privacy Policy", "sms_link": "Text Messaging (SMS)",
    "sms_short": "By texting us, you agree to receive text messages from Reliable Automotive Services about your service. Message frequency varies. Msg &amp; data rates may apply. Reply STOP to opt out, HELP for help.",
    "sms_details": "SMS details",
    "footer_tag": "Mobile auto repair &middot; Lubbock County, TX",
    "quick": "Quick contact", "main_nav": "Main", "crumb_label": "Breadcrumb",
    "quote_h": "Get a quote", "quote_p": "Tell us the year, make, model, and what it's doing.",
    "texts_to": "Texts go to", "aside_label": "Get a quote",
    "other_services": "Other services", "nearby": "Nearby areas", "full_area": "Full service area",
    "on_page": "On this page", "legal": "Legal", "effective": "Effective",
    "mobile_service": "Mobile service",
    "og_alt": "Reliable Automotive Services, mobile mechanic, Lubbock TX",
}

HOME = {
    "title": "Mobile Mechanic Lubbock, TX | Reliable Automotive Services",
    "desc": "Lubbock's mobile mechanic. Diagnostics, brakes, batteries, starters, alternators, and maintenance at your home or work across Lubbock County. Call (806) 451-3520.",
    "eyebrow": "Mobile mechanic &middot; Lubbock County, TX",
    "h1a": "We Bring the Shop", "h1b": "To Your Driveway.",
    "lead": "Reliable Automotive Services is Lubbock's mobile mechanic. Diagnostics, brakes, batteries, starters, alternators, cooling systems, and maintenance done at your home, work, or wherever your vehicle is. No tow. No waiting room.",
    "badge_h": "Your Car Guy in the 806",
    "checks": ["We come to you across Lubbock County", "Price before any work starts", "Test first, then replace. No parts guessing.", "Cars, trucks, SUVs &amp; light fleets"],
    "text_btn": "Text a Photo or Question",
    "svc_eyebrow": "What we fix", "svc_h": "Mobile Auto Repair Services",
    "svc_p": "Most of the repairs that send people to a shop can be done right where your vehicle is parked. Here's what we handle on site.",
    "how_eyebrow": "How it works", "how_h": "Fixed in Three Steps",
    "steps": [("Call or text", "Tell us the year, make, model, and what it's doing. Photos and videos of warning lights or noises help."),
              ("Get a price", "We go over the likely fix and give you a price. Nothing gets done until you approve it."),
              ("We come to you", "We show up with the tools and parts, make the repair on site, and show you what we found.")],
    "why_eyebrow": "Why mobile", "why_h": "Skip the Tow, the Ride &amp; the Waiting Room",
    "why_p": ["A trip to a repair shop usually means arranging a ride, losing a day, and sometimes paying for a tow just to get the vehicle there. When the mechanic comes to you, all of that goes away. Your vehicle gets fixed while you keep working, take care of the kids, or relax at home.",
              "We're straight with people. We test before we replace parts, we explain what we found in plain English, and we tell you what needs to be done now and what can wait. If a job really needs a shop lift, we'll tell you that before any work starts."],
    "serving_h": "Serving Lubbock County &amp; nearby towns", "see_area": "See our full service area",
    "faq_eyebrow": "Questions", "faq_h": "Mobile Mechanic FAQ",
}

HOME_FAQ = [
    ("What is a mobile mechanic?", "A mobile mechanic brings the tools, parts, and know-how to wherever your vehicle is (your home, your work, or wherever it broke down) and makes the repair on site. No tow, no waiting room, no ride needed."),
    ("What areas do you serve?", f"We serve Lubbock and the rest of Lubbock County, including Wolfforth, Shallowater, Slaton, Idalou, New Deal, Abernathy, Ransom Canyon, and Buffalo Springs, plus surrounding towns. Call {CALL} if you're not sure we cover your location."),
    ("What kinds of repairs can be done on site?", "Most common repairs: diagnostics, brakes, batteries, starters, alternators, cooling system parts, tune-ups, suspension and steering parts, and maintenance. If a job truly needs a shop, we'll tell you before any work starts."),
    ("How do I get a quote?", f"Call {CALL} or text {TEXT} with your year, make, model, and what the vehicle is doing. We'll go over the job and give you a price before any work begins."),
    ("Do I need to be home while you work?", "Not always. As long as we can reach the vehicle and the keys, and you can approve the work by phone, many jobs can be done while you're at work."),
    ("What do you need from me?", "A safe, reasonably flat place to work, access to the vehicle and keys, and a good description of the problem. Photos or a short video of a noise or warning light help a lot."),
    ("Do you speak Spanish?", "Our website is available in Spanish. Use the language switch at the top of any page or the Language / Idioma setting at the bottom."),
]

SERVICES_PAGE = {
    "title": "Mobile Auto Repair Services in Lubbock, TX | Reliable Automotive",
    "desc": "Mobile auto repair services in Lubbock County: diagnostics, brakes, batteries, starters, alternators, cooling, tune-ups, suspension, inspections, and fleet service.",
    "h1": "Mobile Auto Repair Services", "eyebrow": "Services",
    "lead": "Everything we fix at your home, work, or roadside across Lubbock County and the surrounding towns.",
    "more_h": "Don't see your repair?",
    "more_p": "This list covers the most common jobs, not everything we do. Call {call} or text {text} with your year, make, model, and what's going on, and we'll tell you whether it's a job we can handle on site.",
}

SERVICE_TPL = {"included": "What's included", "where": "Where we do this work",
               "where_p": "We provide {svc} on site across Lubbock County, including {areas}, and surrounding towns. Not sure if we come to you? Call {call}.",
               "faq": "Common questions"}

SERVICES = [
    {
        "key": "check-engine-light-diagnostics", "slug": "check-engine-light-diagnostics", "icon": "engine",
        "name": "Check Engine Light Diagnostics",
        "short": "Check engine light, rough running, stalling, poor fuel mileage, or a warning you can't figure out.",
        "title": "Check Engine Light Diagnostics in Lubbock, TX | Mobile Mechanic",
        "desc": "Mobile check engine light diagnostics in Lubbock. We come to you, find the real cause, and explain the fix before any work starts. Call (806) 451-3520.",
        "h1": "Mobile Check Engine Light Diagnostics in Lubbock",
        "intro": "A code reader tells you where to start looking. It doesn't tell you what's broken. We bring professional scan tools to your driveway, parking lot, or job site, then test the parts and circuits behind the code so you pay to fix the actual problem, not to guess.",
        "covers": ["Reading and interpreting engine, transmission, ABS, and airbag codes", "Live data and freeze-frame review", "Misfires, rough idle, hesitation, and stalling", "Vacuum leaks, sensor faults, and wiring problems", "Evaporative (EVAP) system leaks and loose-gas-cap codes", "A clear explanation of what we found, what it costs to fix, and what can wait"],
        "body": [
            ("Why a code isn't a diagnosis", "A code like P0171 (system too lean) can be caused by a vacuum leak, a dirty mass airflow sensor, a weak fuel pump, or an exhaust leak ahead of the oxygen sensor. Parts stores will hand you the most common part on the list. We test before we replace, which saves you from buying parts you didn't need."),
            ("Is it safe to keep driving?", f"A solid check engine light usually means get it looked at soon. A flashing check engine light means an active misfire that can overheat and ruin the catalytic converter. If yours is flashing, ease off, park it if you can, and call us at {CALL}."),
        ],
        "faq": [
            ("Can you diagnose my check engine light at my house?", "Yes. Diagnostics is one of the jobs best suited to mobile service. We come to your home, work, or wherever the vehicle is parked in Lubbock County and nearby towns."),
            ("Will the light go off after the repair?", "Once the fault is fixed we clear the codes and confirm the system is running correctly. Some monitors need a normal drive cycle to finish their self-tests, and we'll tell you what to expect."),
        ],
    },
    {
        "key": "brake-repair", "slug": "brake-repair", "icon": "brake",
        "name": "Brake Repair",
        "short": "Squealing, grinding, a soft pedal, or shaking when you stop. Pads, rotors, calipers, and lines.",
        "title": "Mobile Brake Repair in Lubbock, TX | Pads, Rotors & Calipers",
        "desc": "Mobile brake repair in Lubbock County: pads, rotors, calipers, hoses, and brake fluid service done at your home or work. Call (806) 451-3520 to schedule.",
        "h1": "Mobile Brake Repair in Lubbock & Surrounding Towns",
        "intro": "Brakes are the one system you can't put off. We inspect the whole system, not just the pads, and fix it right where your vehicle is parked so you don't have to drive on worn-out brakes to get to a shop.",
        "covers": ["Front and rear brake pad replacement", "Rotor replacement", "Caliper and caliper bracket replacement", "Brake hoses and lines", "Brake fluid flush and bleeding", "Brake inspection with measurements you can see"],
        "body": [
            ("Warning signs", "High-pitched squeal when braking (the wear indicator), metal-on-metal grinding, a pedal that sinks or feels spongy, pulling to one side, or a steering wheel that shakes when you stop from highway speed. Grinding means the pad material is gone and the rotor is being damaged with every stop."),
            ("What a brake job should include", "A proper brake job includes cleaning and lubricating the slide pins and pad contact points, checking the hoses, and checking fluid condition, not just slapping new pads on. That's how we do it."),
        ],
        "faq": [
            ("Can brakes really be done in a driveway?", "Yes. Pads, rotors, and calipers on most cars, trucks, and SUVs are done with the vehicle safely on jack stands. We need a reasonably flat, firm surface to work on."),
            ("How do I know if I need rotors too?", "We measure rotor thickness and check for heat damage and scoring. If the rotors are still in spec and true, you won't be sold new ones."),
        ],
    },
    {
        "key": "battery-starter-alternator", "slug": "battery-starter-alternator", "icon": "battery",
        "name": "Battery, Starter & Alternator",
        "short": "Won't start, clicks, slow crank, or battery light on. We test the whole charging system.",
        "title": "Car Won't Start? Battery, Starter & Alternator Repair | Lubbock",
        "desc": "Car won't start in Lubbock? We test the battery, starter, alternator, and cables on site and fix it where it sits. Mobile mechanic service. Call (806) 451-3520.",
        "h1": "Battery, Starter & Alternator Repair That Comes to You",
        "intro": "When a vehicle won't start, the hardest part is getting it somewhere to be fixed. We skip that step. We test the battery, cables, starter, and alternator where the vehicle sits and fix what actually failed.",
        "covers": ["Battery testing and replacement", "Starter replacement", "Alternator and charging system testing and replacement", "Corroded or loose battery cables and terminals", "Parasitic drain testing (battery keeps dying overnight)", "No-crank and crank-no-start diagnosis"],
        "body": [
            ("Battery or alternator?", "If the vehicle starts after a jump and dies again later, the alternator may not be charging. If it starts fine after a jump and then won't start the next morning, look at the battery or something draining it overnight. Either way, testing beats guessing. A new battery won't fix a bad alternator."),
            ("West Texas is hard on batteries", "Summer heat under the hood speeds up battery wear, and the first cold snap is when a weak battery finally gives up. If your battery is getting older and the engine is cranking slower than it used to, have it tested before it strands you."),
        ],
        "faq": [
            ("My car just clicks. What's wrong?", "A single click or rapid clicking usually points to a weak battery, a poor cable connection, or a failing starter. We test each one so you only replace what failed."),
            ("Can you come to a parking lot or my work?", "Yes, as long as we can safely and legally work on the vehicle where it's parked."),
        ],
    },
    {
        "key": "oil-change-maintenance", "slug": "oil-change-maintenance", "icon": "oil",
        "name": "Oil Changes & Maintenance",
        "short": "Oil and filter changes, fluid services, filters, wipers, and mileage-based maintenance at your place.",
        "title": "Mobile Oil Change & Car Maintenance in Lubbock, TX",
        "desc": "Mobile oil changes and scheduled maintenance in Lubbock and surrounding towns. Filters, fluids, and inspections done at your home or business. Call (806) 451-3520.",
        "h1": "Mobile Oil Changes & Scheduled Maintenance",
        "intro": "Skip the waiting room. We handle routine maintenance at your home or workplace and give you an honest look at anything else that's getting close to needing attention.",
        "covers": ["Oil and filter changes (conventional, blend, and full synthetic)", "Engine and cabin air filters", "Coolant, brake, and power steering fluid services", "Wiper blades and bulbs", "Tire pressure check and visual tire inspection", "Multi-point inspection while we're there"],
        "body": [
            ("Follow your manufacturer, not a sticker", "Many newer vehicles call for longer oil change intervals, while trucks that tow, idle a lot, or drive on dusty roads fall under the severe-service schedule. We'll set you up on the schedule that fits how you actually drive."),
            ("Dust is the enemy out here", "Caliche roads and spring dust storms load up air filters faster than the owner's manual assumes. A clogged engine air filter costs you power and fuel mileage. We check it every time."),
        ],
        "faq": [
            ("Do you bring the oil and filter?", "Yes. We bring the correct oil and filter for your vehicle and take the used oil with us for proper recycling."),
            ("Can you service several vehicles at once?", "Yes. Families and businesses often have us knock out more than one vehicle in the same visit."),
        ],
    },
    {
        "key": "cooling-system-repair", "slug": "cooling-system-repair", "icon": "temp",
        "name": "Cooling System & Overheating",
        "short": "Running hot, leaking coolant, or a sweet smell. Radiators, water pumps, thermostats, and hoses.",
        "title": "Overheating Car Repair in Lubbock | Mobile Cooling System Service",
        "desc": "Car overheating in Lubbock? Mobile radiator, water pump, thermostat, and hose repair, plus cooling system pressure testing. Call (806) 451-3520.",
        "h1": "Overheating & Cooling System Repair",
        "intro": "West Texas summers push cooling systems hard. An overheating engine can turn a small leak into a blown head gasket fast, so we find the leak or the failed part and fix it before it becomes an engine replacement.",
        "covers": ["Cooling system pressure testing to locate leaks", "Radiator replacement", "Water pump replacement", "Thermostat and thermostat housing replacement", "Radiator and heater hoses", "Coolant flush and fill with the correct coolant type"],
        "body": [
            ("If the temperature gauge climbs", "Turn off the A/C, turn the heater on full, and get off the road safely. If it keeps climbing, shut the engine off. Never open a hot radiator cap. Pressurized coolant can cause serious burns. Then call us."),
            ("The correct coolant matters", "Mixing coolant types can cause sludge and corrosion. We use the type your engine was designed for."),
        ],
        "faq": [
            ("Is it safe to drive an overheating car to a shop?", "It's risky. Driving an engine that is overheating can warp the cylinder head or blow the head gasket. That's exactly why mobile repair makes sense here."),
            ("Why is my coolant low but I don't see a leak?", "Coolant can leak only under pressure when the engine is hot, or leak internally. A pressure test finds leaks you can't see with the engine cold."),
        ],
    },
    {
        "key": "tune-up-ignition", "slug": "tune-up-ignition", "icon": "spark",
        "name": "Tune-Ups & Ignition",
        "short": "Spark plugs, ignition coils, misfires, and rough idle. Get the power and mileage back.",
        "title": "Mobile Tune-Up, Spark Plugs & Ignition Coils | Lubbock, TX",
        "desc": "Mobile tune-ups in Lubbock: spark plugs, ignition coils, misfire repair, and throttle body cleaning done at your location. Call (806) 451-3520.",
        "h1": "Mobile Tune-Ups, Spark Plugs & Ignition Coils",
        "intro": "Worn spark plugs and failing coils cause misfires, rough idle, hard starts, and poor fuel mileage. We replace them at your place and confirm the misfire is gone before we leave.",
        "covers": ["Spark plug replacement", "Ignition coil diagnosis and replacement", "Misfire diagnosis", "Throttle body cleaning", "Engine air filter replacement", "Rough idle and hesitation diagnosis"],
        "body": [
            ("Today's \"tune-up\"", "Modern engines don't need the points-and-timing tune-ups of the past, but spark plugs still wear out on a schedule, and coils and boots still fail. Done on time, a tune-up keeps the engine running smooth and protects the catalytic converter from misfire damage."),
        ],
        "faq": [
            ("How often should spark plugs be replaced?", "It depends on the engine and plug type. Many modern iridium plugs last around 100,000 miles, while some engines call for them much sooner. We'll check your manufacturer's schedule."),
        ],
    },
    {
        "key": "suspension-steering", "slug": "suspension-steering", "icon": "steer",
        "name": "Suspension & Steering",
        "short": "Clunks, wandering, uneven tire wear, or a bouncy ride. Shocks, struts, tie rods, and more.",
        "title": "Mobile Suspension & Steering Repair in Lubbock, TX",
        "desc": "Mobile suspension and steering repair in Lubbock County: shocks, struts, tie rod ends, ball joints, sway bar links, and wheel bearings. Call (806) 451-3520.",
        "h1": "Suspension & Steering Repair",
        "intro": "Rough county roads wear out suspension parts. Clunks over bumps, a truck that wanders on the highway, or tires wearing on one edge are all signs something is loose or worn.",
        "covers": ["Shocks and struts", "Tie rod ends", "Ball joints and control arms", "Sway bar links and bushings", "Wheel bearings and hub assemblies", "Steering and suspension inspection"],
        "body": [
            ("Plan on an alignment", "Replacing tie rods, control arms, or struts changes alignment angles. After that kind of work you'll need a wheel alignment at an alignment shop to protect your tires. We'll tell you up front when a repair calls for one."),
        ],
        "faq": [
            ("What's that clunk over bumps?", "Common causes are worn sway bar links, ball joints, strut mounts, or control arm bushings. We inspect each one to pin it down."),
        ],
    },
    {
        "key": "pre-purchase-inspection", "slug": "pre-purchase-inspection", "icon": "search",
        "name": "Pre-Purchase Inspections",
        "short": "Buying a used car or truck? We meet you at the seller and check it out before you pay.",
        "title": "Used Car Pre-Purchase Inspection in Lubbock | Mobile Mechanic",
        "desc": "Mobile pre-purchase inspection in Lubbock and surrounding areas. We meet you at the seller and inspect the vehicle before you buy. Call (806) 451-3520.",
        "h1": "Mobile Pre-Purchase Inspections for Used Vehicles",
        "intro": "A used vehicle can look clean and still be hiding expensive problems. We meet you at the seller's house or lot, inspect the vehicle top to bottom, and tell you straight what we found so you can buy with confidence, negotiate, or walk away.",
        "covers": ["Computer scan for stored and pending codes", "Engine and transmission condition and leaks", "Brakes, tires, steering, and suspension", "Cooling system and belts", "Battery and charging system test", "Signs of flood, frame, or collision damage"],
        "body": [
            ("Recently cleared codes are a red flag", "When the battery is disconnected or codes are cleared right before a sale, the vehicle's readiness monitors reset. We check monitor status so a hidden problem doesn't drive off the lot with you."),
        ],
        "faq": [
            ("Do I need to be there for the inspection?", "It helps, but it isn't required as long as the seller allows the inspection. We'll walk you through the findings either way."),
        ],
    },
    {
        "key": "fleet-service", "slug": "fleet-service", "icon": "truck",
        "name": "Fleet & Work Truck Service",
        "short": "Keep work trucks and company vehicles running without taking them off the job.",
        "title": "Mobile Fleet Maintenance in Lubbock, TX | Work Trucks & Vans",
        "desc": "Mobile fleet maintenance and repair for Lubbock-area businesses. We service work trucks, vans, and company cars at your yard. Call (806) 451-3520.",
        "h1": "Mobile Fleet & Work Truck Service",
        "intro": "Every hour a work truck sits at a repair shop costs you money. We service light-duty fleets at your yard or job site so vehicles stay on the road and your people stay working.",
        "covers": ["Scheduled maintenance for light-duty trucks, vans, and cars", "Brakes, batteries, and charging systems", "Check engine light diagnostics", "Pre-trip style inspections", "On-site repairs at your yard or shop", "One point of contact for every vehicle"],
        "body": [
            ("Built around your schedule", "We can service vehicles early, after hours, or on a set rotation so nothing is pulled off the job during working hours. Call to set up a schedule for your fleet."),
        ],
        "faq": [
            ("How many vehicles do I need to set up fleet service?", "There's no minimum. Contractors with two trucks and companies with a full yard are both welcome."),
        ],
    },
]

AREA_PAGE = {
    "title": "Service Area | Mobile Mechanic in Lubbock County, TX",
    "desc": "Reliable Automotive Services is a mobile mechanic covering Lubbock, Wolfforth, Shallowater, Slaton, Idalou, and surrounding towns across Lubbock County, TX.",
    "h1": "Mobile Mechanic Service Area", "eyebrow": "Where we go",
    "lead": "We cover Lubbock, all of Lubbock County, and the surrounding West Texas towns.",
    "card_more": "Mobile service in {town}",
    "also_h": "Also serving surrounding towns",
    "also_p": "Beyond the towns above, we regularly travel to {towns}. If you're outside these areas, call {call}. Depending on the job and our schedule, we may still be able to come to you.",
    "and": "and",
}

AREA_TPL = {
    "h_repair": "Auto repair at your place in {town}", "h_services": "Services available in {town}",
    "h_faq": "Questions from {town} drivers",
    "faq": [("Do you come to {town}?", "Yes. {town} is in our regular service area. Call {call} or text {text} to schedule."),
            ("What repairs can you do in {town}?", "Diagnostics, brakes, batteries, starters, alternators, cooling system repairs, tune-ups, suspension and steering, pre-purchase inspections, and routine maintenance, all on site.")],
    "schema_name": "Mobile mechanic in {town}, TX",
}

AREAS = [
    {"key": "lubbock", "slug": "lubbock", "name": "Lubbock",
     "title": "Mobile Mechanic in Lubbock, TX | Reliable Automotive Services",
     "desc": "Mobile mechanic in Lubbock, TX. Diagnostics, brakes, batteries, starters, alternators, and maintenance done at your home or work. Call (806) 451-3520.",
     "h1": "Mobile Mechanic in Lubbock, Texas",
     "intro": "From South Lubbock to North Overton, near Texas Tech to the edges of town along Loop 289, we bring the shop to you. Most of our calls are right here in Lubbock: driveways, apartment lots, and workplaces across the city.",
     "local": "Lubbock drivers rack up a lot of miles on the Loop, the Marsha Sharp Freeway, and the long highway runs to the surrounding towns. Heat, dust, and stop-and-go traffic wear on batteries, brakes, and cooling systems. We see those repairs every week and handle them on site.",
     "nearby": ["wolfforth", "shallowater", "idalou", "slaton"]},
    {"key": "wolfforth", "slug": "wolfforth", "name": "Wolfforth",
     "title": "Mobile Mechanic in Wolfforth, TX | Reliable Automotive Services",
     "desc": "Mobile auto repair in Wolfforth, TX. We come to your home or business for diagnostics, brakes, battery and starter work, and maintenance. Call (806) 451-3520.",
     "h1": "Mobile Mechanic Serving Wolfforth, TX",
     "intro": "Wolfforth sits just southwest of Lubbock along US-62/82, and a lot of its families drive into the city every day. Save yourself a round trip to a repair shop and a ride back. We come out to Wolfforth and handle the repair in your driveway.",
     "local": "Commuter vehicles and family SUVs make up most of what we see in Wolfforth: brakes, batteries, oil changes, and check engine lights. Call ahead and we'll schedule a time that works around school and work.",
     "nearby": ["lubbock", "shallowater"]},
    {"key": "shallowater", "slug": "shallowater", "name": "Shallowater",
     "title": "Mobile Mechanic in Shallowater, TX | Reliable Automotive Services",
     "desc": "Mobile mechanic in Shallowater, TX for farm trucks, family vehicles, and work trucks. Diagnostics, brakes, batteries, and maintenance. Call (806) 451-3520.",
     "h1": "Mobile Mechanic Serving Shallowater, TX",
     "intro": "Northwest of Lubbock on US-84, Shallowater is farm and ranch country, and that means pickups that work hard. We come out to your house, farm, or shop and get your vehicle running without you losing half a day hauling it into town.",
     "local": "Dusty county roads are hard on air filters, wheel bearings, and suspension parts, and farm trucks often sit through the slow season and then need to start on the first try. We handle diagnostics, batteries, starters, brakes, and maintenance on site.",
     "nearby": ["lubbock", "wolfforth"]},
    {"key": "slaton", "slug": "slaton", "name": "Slaton",
     "title": "Mobile Mechanic in Slaton, TX | Reliable Automotive Services",
     "desc": "Mobile auto repair in Slaton, TX. Diagnostics, brakes, batteries, alternators, and maintenance at your home or business. Call (806) 451-3520.",
     "h1": "Mobile Mechanic Serving Slaton, TX",
     "intro": "Slaton is southeast of Lubbock on US-84, and when a vehicle won't start out there, the trip to a city shop is the hardest part. We come to you instead.",
     "local": "Whether it's a work truck, a family car, or a vehicle you're thinking about buying, we can diagnose it, repair it, or inspect it right where it sits in Slaton.",
     "nearby": ["lubbock", "idalou"]},
    {"key": "idalou", "slug": "idalou", "name": "Idalou",
     "title": "Mobile Mechanic in Idalou, TX | Reliable Automotive Services",
     "desc": "Mobile mechanic in Idalou, TX. On-site diagnostics, brake repair, battery and starter replacement, and maintenance. Call (806) 451-3520.",
     "h1": "Mobile Mechanic Serving Idalou, TX",
     "intro": "Idalou sits east of Lubbock on US-62/82. Instead of towing your vehicle into the city, let us come out to your home, farm, or business in Idalou and fix it there.",
     "local": "We handle the repairs rural drivers need most, like no-start problems, brakes, charging systems, and maintenance on pickups and family vehicles, without the tow bill.",
     "nearby": ["lubbock", "slaton"]},
]

ABOUT = {
    "title": "About Reliable Automotive Services | Lubbock Mobile Mechanic",
    "desc": "Meet Reliable Automotive Services, the Lubbock mobile mechanic known as Your Car Guy 806. Honest diagnosis, upfront pricing, and repairs at your location.",
    "h1": "About Reliable Automotive Services", "eyebrow": "About us",
    "lead": "A Lubbock mobile mechanic built on doing the job right and being straight with people.",
    "html": """<h2>Local, mobile, and reliable</h2>
<p>Reliable Automotive Services is a West Texas auto repair business with a simple idea: most repairs don't need you to bring your vehicle to us. We bring the tools, the parts, and the experience to your driveway, your job site, or wherever your vehicle is parked across Lubbock County and the surrounding towns.</p>
<p>People call us &ldquo;Your Car Guy&rdquo; because that's what we want to be: the person you call first when something sounds wrong, a light comes on, or the truck won't start.</p>
<h2>How we work</h2>
<ul class="checks">
<li><strong>Diagnose before we replace.</strong> We test the parts and circuits behind a problem instead of throwing parts at it.</li>
<li><strong>Price before work.</strong> You approve the job and the price before we start.</li>
<li><strong>Plain-English explanations.</strong> You'll know what failed, why, and what can wait.</li>
<li><strong>Straight answers.</strong> If a repair really needs a shop, we'll tell you up front.</li>
</ul>
<h2>Who we work on</h2>
<p>Daily drivers, family SUVs, pickups, farm trucks, and light-duty work fleets. If you're not sure we can help with your vehicle, call {call_link} and ask.</p>""",
}

CONTACT = {
    "title": "Contact & Request Service | Reliable Automotive Services Lubbock",
    "desc": "Request mobile auto repair in Lubbock County. Call (806) 451-3520, text (806) 776-4460, or send a service request and we'll get back to you with a price.",
    "h1": "Request Mobile Service", "eyebrow": "Contact",
    "lead": "Call, text, or fill out the form and we'll get back to you with a price.",
    "form_h": "Service request",
    "hint": "Submitting opens a pre-filled text message to {text} on your phone. Just hit send. On a computer? Use &ldquo;Copy request&rdquo; and text it to {text}, or call {call}.",
    "name": "Name", "phone": "Callback number", "vehicle": "Year, make &amp; model", "service": "Service needed",
    "not_sure": "Not sure / other", "location": "Where is the vehicle?", "location_ph": "Town or cross streets",
    "when": "Best time", "when_ph": "e.g. Thursday afternoon", "details": "What's it doing?",
    "details_ph": "Noises, warning lights, when it started...", "vehicle_ph": "2016 Chevy Silverado 1500",
    "submit": "Text My Request", "copy": "Copy request",
    "area_h": "Service area", "area_p": "Lubbock, all of Lubbock County, and surrounding towns.", "area_link": "See the full list",
}

NOT_FOUND = {"title": "Page Not Found | Reliable Automotive Services", "desc": "Page not found.",
             "eyebrow": "Error 404", "h1": "This Page Broke Down.",
             "lead": "The page you're looking for isn't here. Good news: your vehicle can still get fixed.",
             "home": "Back to Home", "popular": "Popular services"}

# JS strings for the request form (rendered as data attributes)
FORM_JS = {
    "intro": "Service request from yourcarguy806.com",
    "labels": "Name|Callback|Vehicle|Service|Location|Best time|Details",
    "missing": "Please add {list}.",
    "m_name": "your name", "m_phone": "a 10-digit callback number", "m_vehicle": "your vehicle", "m_location": "where the vehicle is",
    "copied": "Copied. Paste it into a text to (806) 776-4460.", "copy_prompt": "Copy your request:",
    "m_consent": "Please check the box to agree to receive text messages, or call (806) 451-3520 instead.",
    "lang_line": "",
}

EFFECTIVE = "November 3, 2026"

TERMS = {
    "title": "Terms of Service | Reliable Automotive Services",
    "desc": "Terms of Service for Reliable Automotive Services, a mobile mechanic in Lubbock, TX: estimates, authorization, parts, payment, warranty, and liability.",
    "h1": "Terms of Service", "lead": "The terms that apply to our website and mobile repair services.",
    "sections": [
        ("Who we are", "<p>These Terms of Service (&ldquo;Terms&rdquo;) apply to the website yourcarguy806.com and to automotive repair and maintenance services provided by Reliable Automotive Services (&ldquo;we,&rdquo; &ldquo;us,&rdquo; &ldquo;our&rdquo;), a mobile auto repair business based in Lubbock, Texas. By using this website or scheduling service with us, you agree to these Terms.</p>"),
        ("Website information", "<p>Content on this site is general information about our services and common vehicle problems. It is not a diagnosis of your vehicle. Every vehicle is different, and only an inspection can confirm what it needs. We may update services, descriptions, and service areas at any time.</p>"),
        ("Quotes and estimates", "<p>Prices given by phone, text, or in person are estimates based on the information available at the time. If we find that the vehicle needs more or different work than expected, we will contact you and get your approval before doing any additional work that changes the price. Diagnostic time may be charged even if you decide not to go ahead with the repair. We will tell you about any diagnostic charge before we start.</p>"),
        ("Authorization", "<p>By approving a repair, verbally, in writing, or by text, you confirm that you own the vehicle or are authorized by the owner to approve work on it, and you authorize us to perform the approved work, including test drives where needed to diagnose or verify a repair.</p>"),
        ("Work location and access", "<ul><li>You are responsible for providing a safe, reasonably level place to work where you have the right to allow vehicle repairs, along with access to the vehicle and keys.</li><li>You are responsible for complying with any HOA, apartment, landlord, or employer rules about repairs on the property.</li><li>We may decline, pause, or reschedule work if conditions are unsafe, including weather, traffic, an unsafe surface, or unsafe surroundings.</li><li>Some repairs cannot be done safely or properly outside a shop. If that's the case, we'll tell you before starting.</li></ul>"),
        ("Parts", "<p>We source parts appropriate to the repair unless we agree otherwise. Parts warranties are provided by the part manufacturer or supplier and are passed through to you. If you supply your own parts, we are not responsible for their quality, fit, or failure, and labor to diagnose or replace customer-supplied parts that fail is billable. Replaced parts are disposed of unless you ask to keep them before work begins.</p>"),
        ("Payment", "<p>Payment is due when the work is completed unless we have agreed to other terms in writing. Accepted payment methods will be confirmed when you schedule. We may require a deposit for special-order parts. Returned payments may be subject to fees allowed by Texas law.</p>"),
        ("Warranty", "<p>Any warranty on our labor will be stated on your invoice or written estimate. Warranties do not cover damage from accidents, abuse, neglect, racing, off-road use, lack of maintenance, other shops' work, or pre-existing conditions unrelated to the repair. If you believe a repair has failed, contact us first so we can inspect it.</p>"),
        ("Pre-existing conditions", "<p>Older vehicles may have worn, rusted, seized, or brittle parts. Fasteners, sensors, connectors, and lines can break during normal removal even when handled with care. We will tell you right away if this happens and will not be responsible for parts that fail because of their prior condition. We are not responsible for personal items left in the vehicle.</p>"),
        ("Inspections", "<p>Pre-purchase and general inspections are a visual and functional evaluation of the vehicle's condition at the time of the inspection. They are not a guarantee of future performance and cannot detect every hidden or intermittent problem.</p>"),
        ("Limitation of liability", "<p>To the fullest extent allowed by law, our total liability for any claim related to our services is limited to the amount you paid for the specific service involved. We are not liable for indirect or consequential losses such as loss of use, rental costs, towing, lost wages, or lost profits, except where Texas law does not allow such limits.</p>"),
        ("Text messages (SMS)", "<p>Our text line is {text_link}. Customers start the conversation: when you text us, or send a service request from our website (which opens a text to us from your phone), you agree to receive text messages from Reliable Automotive Services about your request, quotes and estimates, appointments, repair status, and receipts. We do not send marketing texts.</p><ul><li>Message frequency varies with your service.</li><li>Message and data rates may apply.</li><li>Reply <strong>STOP</strong> at any time to opt out. You'll get one confirmation and no more texts.</li><li>Reply <strong>HELP</strong> for help, or call {call_link}.</li><li>Consent to receive texts is not a condition of any purchase.</li><li>Carriers are not liable for delayed or undelivered messages.</li></ul><p>Full details are on our <a href=\"/sms/\">Text Messaging (SMS)</a> page. See also our <a href=\"/privacy/\">Privacy Policy</a>.</p>"),
        ("Language", "<p>These Terms are provided in English and Spanish for your convenience. If there is any conflict between the two versions, the English version controls.</p>"),
        ("Governing law", "<p>These Terms are governed by the laws of the State of Texas. Any dispute will be handled in the courts located in Lubbock County, Texas, unless the law requires otherwise.</p>"),
        ("Changes", "<p>We may update these Terms from time to time. The effective date at the top of this page shows when they last changed. The version in effect when you schedule service applies to that service.</p>"),
        ("Contact", "<p>Questions about these Terms? Call {call_link} or text {text_link}.</p>"),
    ],
}

PRIVACY = {
    "title": "Privacy Policy | Reliable Automotive Services",
    "desc": "Privacy Policy for Reliable Automotive Services in Lubbock, TX. No ad trackers, no selling your data. How we use the information you share with us.",
    "h1": "Privacy Policy", "lead": "What we collect, why, and how we protect it.",
    "sections": [
        ("Overview", "<p>This Privacy Policy explains what information Reliable Automotive Services collects through yourcarguy806.com and when you contact us or use our services, and how we use it. We keep it simple: we collect only what we need to fix your vehicle and run our business, and we don't sell your information.</p>"),
        ("Information you give us", "<p>When you call, text, or send a service request, you may give us your name, phone number, the location of your vehicle, vehicle details (year, make, model, VIN, mileage), a description of the problem, and photos or videos. When you pay, we receive the payment information needed to process it.</p>"),
        ("How the service request form works", "<p>The request form on our Contact page does not send your information to our website or store it on a server. When you press &ldquo;Text My Request,&rdquo; the form opens the messaging app on your own device with your details pre-filled and addressed to our text line, (806) 776-4460. Nothing is sent until you hit send. &ldquo;Copy request&rdquo; copies the text to your device's clipboard only.</p>"),
        ("Language preference", "<p>If you choose a language on our site, your browser remembers that choice on your device (local storage) so the site opens in the same language next time. It is not sent to us, and you can change it any time.</p>"),
        ("Information collected automatically", "<p>This website does not use advertising trackers, analytics cookies, or third-party marketing pixels. Our hosting and security provider, Cloudflare, processes basic technical information such as IP addresses, browser type, and the pages requested in order to deliver the site and protect it from abuse. See Cloudflare's privacy policy for how it handles that data. If we add analytics in the future, we will update this policy first.</p>"),
        ("How we use information", "<ul><li>To respond to your request and give you a quote</li><li>To schedule, travel to, and perform service on your vehicle</li><li>To send invoices, receipts, and service records, and to process payments</li><li>To follow up on completed work and warranty questions</li><li>To meet legal, tax, and accounting obligations</li></ul>"),
        ("How we share information", "<p>We do not sell or rent your personal information. We share it only as needed to serve you, such as with parts suppliers (vehicle details for ordering parts), payment processors, and our accounting and shop-management software providers, or when required by law. These providers may only use your information to provide services to us.</p>"),
        ("Text messages (SMS)", "<p>Phone numbers and messages you send us are used only to communicate about your service. <strong>No mobile information will be shared with third parties or affiliates for marketing or promotional purposes.</strong> Text messaging originator opt-in data and consent are excluded from every category of sharing described in this policy and will not be shared with any third parties. Reply STOP to stop receiving texts from us, or HELP for help. See our <a href=\"/sms/\">Text Messaging (SMS)</a> page.</p>"),
        ("Data retention and security", "<p>We keep customer and vehicle service records for as long as needed to support warranties and your vehicle's service history, and to meet our legal and tax obligations. We use reasonable safeguards to protect your information, but no method of storage or transmission is completely secure.</p>"),
        ("Your choices", "<p>You can ask us what information we have about you, ask us to correct it, or ask us to delete it, subject to records we are legally required to keep. Call {call_link} or text {text_link}.</p>"),
        ("Children", "<p>Our website and services are intended for adults. We do not knowingly collect personal information from children under 13.</p>"),
        ("Language", "<p>This Privacy Policy is provided in English and Spanish. If there is any conflict between the two versions, the English version controls.</p>"),
        ("Changes", "<p>We may update this Privacy Policy from time to time. The effective date at the top of the page shows when it last changed.</p>"),
        ("Contact", "<p>Questions about privacy? Call {call_link} or text {text_link}.</p>"),
    ],
}

SMS_PAGE = {
    "title": "Text Us | SMS Terms & Consent | Reliable Automotive Services",
    "desc": "Text Reliable Automotive Services at (806) 776-4460 for quotes, scheduling, and repair updates. How our text messages work, consent, STOP and HELP.",
    "eyebrow": "Text messaging (SMS)",
    "h1": "Text Us at (806) 776-4460",
    "lead": "Get a quote, schedule service, and get repair updates by text message.",
    "cta_h": "Start a text",
    "cta_p": "Text us your name, your vehicle's year, make, and model, where it is, and what it's doing. Photos and videos help.",
    "cta_btn": "Text (806) 776-4460",
    "form_btn": "Use the request form",
    "consent_h": "Consent to receive text messages",
    "consent": "By texting Reliable Automotive Services at (806) 776-4460, or by sending a service request from our website, you agree to receive text messages from Reliable Automotive Services about your service request, quotes and estimates, appointments, repair status, and receipts. Message frequency varies. Message and data rates may apply. Reply STOP to opt out at any time. Reply HELP for help. Consent is not a condition of purchase. Carriers are not liable for delayed or undelivered messages.",
    "sections": [
        ("Program", "<p><strong>Reliable Automotive Services customer care texts.</strong> We text customers who contact us about vehicle repair and maintenance in Lubbock County, Texas, and surrounding towns. Texts are conversational and about your own service. We do not send marketing or promotional texts.</p>"),
        ("How you opt in", "<p>You opt in by texting us first at {text_link}, or by submitting the service request form on our <a href=\"/contact/\">Contact page</a>. The form opens a pre-filled text to us on your phone, and nothing is sent until you hit send. The form also asks you to check a box agreeing to receive texts. We never add numbers to a text list from a purchased or shared list.</p>"),
        ("What we send", "<ul><li>Replies to your questions and requests</li><li>Quotes, estimates, and approval requests</li><li>Appointment scheduling, reminders, and arrival updates</li><li>Repair status updates and receipts</li></ul><p>Example: &ldquo;Reliable Automotive: Hi Sam, your brake estimate is ready: $289 for front pads and rotors. Reply YES to approve. Reply STOP to opt out.&rdquo;</p>"),
        ("Message frequency and cost", "<p>Message frequency varies depending on your service, usually a few messages per job. Message and data rates may apply according to your mobile plan.</p>"),
        ("Opting out and getting help", "<p>Reply <strong>STOP</strong> to any message to opt out. You'll receive one confirmation text and no further messages. Reply <strong>START</strong> to opt back in. Reply <strong>HELP</strong> for help, or call {call_link}.</p>"),
        ("Privacy", "<p><strong>No mobile information will be shared with third parties or affiliates for marketing or promotional purposes.</strong> Text messaging originator opt-in data and consent will not be shared with any third parties. See our <a href=\"/privacy/\">Privacy Policy</a> and <a href=\"/terms/\">Terms of Service</a>.</p>"),
        ("Carriers", "<p>Carriers are not liable for delayed or undelivered messages. Consent to receive texts is not a condition of purchasing any goods or services. You can always call us at {call_link} instead.</p>"),
    ],
}
